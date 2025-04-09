from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    create_refresh_token,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies,
)
from models import db, User
import os
from cryptography.fernet import Fernet

user_bp = Blueprint("user_bp", __name__)


def get_cipher():
    key = os.environ.get("ENCRYPTION_KEY")
    if not key:
        raise ValueError("ENCRYPTION_KEY wurde nicht gesetzt!")
    return Fernet(key.encode())


def encrypt(plaintext: str) -> str:
    cipher = get_cipher()
    return cipher.encrypt(plaintext.encode()).decode()


def decrypt(ciphertext: str) -> str:
    cipher = get_cipher()
    return cipher.decrypt(ciphertext.encode()).decode()


@user_bp.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Invalid JSON data"}), 400

    existing_user = User.query.filter_by(email=data["email"]).first()
    if existing_user:
        return jsonify({"error": "User with this email already exists"}), 409

    new_user = User(
        email=data["email"],
        password=data["password"],  # Use the password setter to hash the password
        first_name=encrypt(data["first_name"]),
        last_name=encrypt(data["last_name"]),
        street=encrypt(data["street"]),
        house_number=encrypt(data["house_number"]),
        postal_code=encrypt(data["postal_code"]),
        city=encrypt(data["city"]),
        country=encrypt(data["country"]),
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return (
            jsonify(
                {"message": "User registered successfully", "user_id": str(new_user.id)}
            ),
            201,
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while registering the user"}), 500


@user_bp.route("/login", methods=["POST"])
def login_user():
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Invalid JSON data"}), 400

    user = User.query.filter_by(email=data["email"]).first()

    try:
        if user and user.check_password(data["password"]):
            # Zusätzliche Benutzerdaten zum Token hinzufügen
            additional_claims = {
                "email": user.email,
                "first_name": decrypt(user.first_name),
                "last_name": decrypt(user.last_name)
            }

            access_token = create_access_token(identity=user.id, additional_claims=additional_claims)
            refresh_token = create_refresh_token(identity=user.id)

            response = jsonify(
                {"message": "Login erfolgreich", "access_token": access_token}
            )
            set_access_cookies(response, access_token)
            set_refresh_cookies(response, refresh_token)
            return response
    except ValueError as e:
        return jsonify({"error": "Invalid password hash"}), 500

    return jsonify({"message": "Invalid credentials"}), 400


@user_bp.route("/user", methods=["GET"])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if user is None:
        return jsonify({"error": "User not found"}), 404

    return (
        jsonify(
            {
                "id": str(user.id),
                "email": user.email,
                "first_name": decrypt(user.first_name),
                "last_name": decrypt(user.last_name),
                "street": decrypt(user.street),
                "house_number": decrypt(user.house_number),
                "postal_code": decrypt(user.postal_code),
                "city": decrypt(user.city),
                "country": decrypt(user.country),
            }
        ),
        200,
    )

@user_bp.route("/user", methods=["PUT"])
@jwt_required()
def update_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.json
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400

    def update_field(field_name):
        value = data.get(field_name)
        if value:  # Wert ist nicht None und nicht leer
            setattr(user, field_name, encrypt(value))

    update_field("first_name")
    update_field("last_name")
    update_field("street")
    update_field("house_number")
    update_field("postal_code")
    update_field("city")
    update_field("country")

    try:
        db.session.commit()

        # Neuen Token mit aktualisierten Benutzerdaten erstellen
        additional_claims = {
            "email": user.email,
            "first_name": decrypt(user.first_name),
            "last_name": decrypt(user.last_name)
        }

        # Neuen Access-Token erstellen und in Cookies setzen
        access_token = create_access_token(identity=user.id, additional_claims=additional_claims)

        response = jsonify({
            "message": "User updated successfully",
            "access_token": access_token,
            "user": {
                "email": user.email,
                "first_name": decrypt(user.first_name),
                "last_name": decrypt(user.last_name)
            }
        })

        # Neuen Token in Cookies setzen
        set_access_cookies(response, access_token)

        return response, 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@user_bp.route("/user", methods=["DELETE"])
@jwt_required()
def delete_current_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if user is None:
        return jsonify({"error": "User not found"}), 404

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while deleting the user"}), 500


@user_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh_token():
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=user_id)

    response = jsonify({"access_token": access_token})
    set_access_cookies(response, access_token)
    return response


@user_bp.route("/logout", methods=["POST"])
def logout_user():
    response = jsonify({"message": "Logout erfolgreich"})
    unset_jwt_cookies(response)
    return response
