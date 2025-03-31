from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token, set_access_cookies, set_refresh_cookies, unset_jwt_cookies
from models  import db, User
from uuid import UUID

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Invalid JSON data"}), 400

    if not data.get('email') or not data.get('password'):
        return jsonify({"error": "Email and password are required"}), 400

        # Prüfen, ob der Benutzer bereits existiert
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({"error": "User with this email already exists"}), 409  # 409 Conflict

    new_user = User(email=data['email'], password=data['password'])

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully", "user_id": str(new_user.id)}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while registering the user"}), 500

@user_bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()

    if data is None:
        return jsonify({"error": "Invalid JSON data"}), 400

    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        response = jsonify({
            "message": "Login erfolgreich",
            "access_token": access_token  # Access-Token im JSON-Response hinzufügen
        })
        set_access_cookies(response, access_token)  # Access-Token im Cookie speichern
        set_refresh_cookies(response, refresh_token)  # Refresh-Token im Cookie speichern
        return response
    return jsonify({"message": "Invalid credentials"}), 400

@user_bp.route('/user', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if user is None:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": str(user.id),
        "email": user.email
    }), 200

@user_bp.route('/user', methods=['DELETE'])
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

@user_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)  # Nur mit Refresh-Token zugänglich
def refresh_token():
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=user_id)

    response = jsonify({"access_token": access_token})  # Return the new access token
    set_access_cookies(response, access_token)  # Neues Access-Token im Cookie speichern
    return response

@user_bp.route('/logout', methods=['POST'])
def logout_user():
    response = jsonify({"message": "Logout erfolgreich"})
    unset_jwt_cookies(response)  # Entfernt Access- und Refresh-Token-Cookies
    return response

