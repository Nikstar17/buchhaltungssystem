from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Document, Upload, LineItem, db

documents_bp = Blueprint('documents_bp', __name__)

@documents_bp.route('/documents', methods=['GET'])
@jwt_required()
def get_documents():
    user_id = get_jwt_identity()
    documents = Document.query.filter_by(user_id=user_id).all()
    result = [
        {
            "id": str(doc.id),
            "document_type": doc.document_type,
            "status": doc.status,
            "number": doc.number,
            "document_date": doc.document_date,
            "supplier_id": doc.supplier_id,
            "delivery_date": doc.delivery_date,
            "link_id": doc.link_id,
            "due_date": doc.due_date,
            "cost_center_id": doc.cost_center_id,
            "currency_code": doc.currency_code,
        }
        for doc in documents
    ]
    return jsonify(result), 200

@documents_bp.route('/documents', methods=['POST'])
@jwt_required()
def set_document():
    user_id = get_jwt_identity()
    data = request.form

    print("Received data:", data)

    if data is None:
        return jsonify({"error": "Invalid JSON data"}), 400

    def parse_uuid_or_none(value):
        return value if value not in ('', 'null', None) else None

    new_document = Document(
        user_id=user_id,
        document_type=data['document_type'],
        status=data['status'],
        number=data['number'],
        document_date=data['document_date'],
        supplier_id=data['supplier_id'],
        delivery_date=data['delivery_date'],
        link_id=parse_uuid_or_none(data['link_id']),
        due_date=data['due_date'] or None,
        cost_center_id=parse_uuid_or_none(data['cost_center_id']),
        currency_code=data['currency_code']
    )

    try:
        db.session.add(new_document)
        db.session.commit()

        new_upload = Upload(
            document_id=new_document.id,
            filename=data['filename'],
            file_path=data['file_path'],
            mimetype=data['mimetype'],
            file_size=data['file_size']
        )

        db.session.add(new_upload)
        db.session.commit()

        positions = request.form.get('positions')
        if positions:
            import json
            positions = json.loads(positions)
            for position in positions:
                new_line_item = LineItem(
                    document_id=new_document.id,
                    line_number=position['line_number'],
                    description=position['description'],
                    quantity=position['quantity'],
                    unit_price=position['unit_price'],
                    total_price=position['total_price'],
                    category_id=parse_uuid_or_none(position['category_id']),
                    tax_rate_id=position['tax_rate_id'],
                    account_id=parse_uuid_or_none(position['account_id'])
                )
                db.session.add(new_line_item)

        db.session.commit()

        return jsonify({"message": "Document, upload, and line items added successfully"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred while adding new Document: {str(e)}"}), 500


@documents_bp.route('/documents/<id>', methods=['GET'])
@jwt_required()
def get_document_by_id(id):
    user_id = get_jwt_identity()
    document = Document.query.filter_by(id=id, user_id=user_id).first()

    if not document:
        return jsonify({"error": "Document not found"}), 404

    result = {
        "id": str(document.id),
        "filename": document.filename,
        "upload_path": document.upload_path,
        "upload_date": document.upload_date,
        "beleg_datum": document.beleg_datum,
        "betrag": float(document.betrag) if document.betrag else None,
        "kategorie_id": str(document.kategorie_id) if document.kategorie_id else None,
        "beschreibung": document.beschreibung,
        "steuerart": document.steuerart
    }
    return jsonify(result), 200

@documents_bp.route('/documents/<id>', methods=['PUT'])
@jwt_required()
def update_document(id):
    user_id = get_jwt_identity()
    document = Document.query.filter_by(id=id, user_id=user_id).first()

    if not document:
        return jsonify({"error": "Document not found"}), 404

    data = request.json
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400

    beschreibung = data.get('beschreibung')
    kategorie_id = data.get('kategorie_id')
    beleg_datum = data.get('beleg_datum')
    betrag = data.get('betrag')
    steuerart = data.get('steuerart')

    # Validate required fields
    if not beschreibung or not beleg_datum or not betrag or not steuerart:
        return jsonify({"error": "All fields (beschreibung, beleg_datum, betrag, steuerart) are required"}), 400

    # Validate kategorie_id as a valid UUID or None
    if kategorie_id == "":
        kategorie_id = None
    elif kategorie_id:
        try:
            from uuid import UUID
            kategorie_id = UUID(kategorie_id)
        except ValueError:
            return jsonify({"error": "Invalid kategorie_id format"}), 400

    # Update document fields
    document.beschreibung = beschreibung
    document.kategorie_id = kategorie_id
    document.beleg_datum = beleg_datum
    document.betrag = betrag
    document.steuerart = steuerart

    try:
        db.session.commit()
        return jsonify({"message": "Document updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@documents_bp.route('/documents/<id>', methods=['DELETE'])
@jwt_required()
def delete_document(id):
    user_id = get_jwt_identity()
    document = Document.query.filter_by(id=id, user_id=user_id).first()

    if not document:
        return jsonify({"error": "Document not found"}), 404

    try:
        db.session.delete(document)
        db.session.commit()
        return jsonify({"message": "Document deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
