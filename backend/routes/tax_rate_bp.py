from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import db, TaxRate

tax_rate_bp = Blueprint('tax_rate_bp', __name__)

@tax_rate_bp.route('/tax_rates', methods=['GET'])
@jwt_required()
def get_tax_rates():
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({'error': 'Benutzer-ID erforderlich'}), 400

    tax_rates = TaxRate.query.filter(
        (TaxRate.user_id == user_id) | (TaxRate.user_id.is_(None)),
        TaxRate.active == True
    ).all()

    return jsonify([{
        'id': str(tax_rate.id),
        'name': tax_rate.name,
        'percentage': float(tax_rate.percentage)
    } for tax_rate in tax_rates])


@tax_rate_bp.route('/tax_rates', methods=['POST'])
@jwt_required()
def set_tax_rate():
    data = request.get_json()
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({'error': 'Benutzer-ID erforderlich'}), 400

    new_tax_rate = TaxRate(
        name=data['name'],
        percentage=data['percentage'],
        valid_from=data['valid_from'],
        active=True,
        user_id=user_id
    )

    try:
        db.session.add(new_tax_rate)
        db.session.commit()
        return jsonify({"message": "New Taxrate successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while adding new Taxrate"}), 400
