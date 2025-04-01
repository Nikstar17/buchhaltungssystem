from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Supplier, db

supplier_bp = Blueprint('supplier_bp', __name__)

@supplier_bp.route('/suppliers', methods=['GET'])
@jwt_required()
def get_suppliers():
    user_id = get_jwt_identity()
    supplier = Supplier.query.filter_by(user_id=user_id).all()
    result = [
        {
            "id": str(sup.id),
            "name": str(sup.name),
            "address": str(sup.address),
            "tax_number": str(sup.tax_number),
            "vat_id": str(sup.vat_id),
            "iban": str(sup.iban),
            "bic": str(sup.bic),
            "email": str(sup.email),
            "phone": str(sup.phone),
        }
        for sup in supplier
    ]
    return jsonify(result), 200

@supplier_bp.route('/suppliers', methods=['POST'])
@jwt_required()
def set_supplier():
    user_id = get_jwt_identity()
    data = request.get_json()
    if not user_id:
        return jsonify({'error': 'Benutzer-ID erforderlich'}), 400

    new_supplier = Supplier(
        user_id=user_id,
        name=data['name'],
        address=data['address'],
        tax_number=data['tax_number'],
        vat_id=data['vat_id'],
        iban=data['iban'],
        bic=data['bic'],
        email=data['email'],
        phone=data['phone'],
    )

    try:
        db.session.add(new_supplier)
        db.session.commit()
        return jsonify({"message": "New Supplier successfully added"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while adding new Supplier"})
