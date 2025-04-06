from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import LineItem, db

line_items_bp = Blueprint('line_items_bp', __name__)

@line_items_bp.route('/documents/<uuid:document_id>/line_items', methods=['GET'])
@jwt_required()
def get_line_items(document_id):
    """
    Fetch all line items associated with a specific document.
    """
    try:
        # Get the current user identity
        current_user = get_jwt_identity()

        # Query the line items for the given document ID
        line_items = LineItem.query.filter_by(document_id=document_id).all()

        # Serialize the line items
        line_items_data = [
            {
                "id": item.id,
                "line_number": item.line_number,
                "description": item.description,
                "quantity": float(item.quantity),
                "unit_price": float(item.unit_price),
                "total_price": float(item.total_price),
                "category_id": item.category_id,
                "tax_rate_id": item.tax_rate_id
            }
            for item in line_items
        ]

        return jsonify({"line_items": line_items_data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
