import os
from werkzeug.utils import secure_filename
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Document, Upload, LineItem, db

UPLOAD_FOLDER = 'uploads'  # Ordner, in dem die Dateien gespeichert werden
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}  # Erlaubte Dateitypen

# Stelle sicher, dass der Upload-Ordner existiert
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
    file = request.files.get('file')  # Datei aus dem Request abrufen

    if data is None or file is None:
        return jsonify({"error": "Invalid form data or missing file"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed"}), 400

    # Sicheren Dateinamen generieren
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    try:
        # Datei speichern
        file.save(file_path)

        def parse_uuid_or_none(value):
            return value if value not in ('', 'null', None) else None

        # Neues Dokument erstellen
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

        db.session.add(new_document)
        db.session.commit()

        # Upload-Daten speichern
        new_upload = Upload(
            document_id=new_document.id,
            filename=filename,
            file_path=file_path,
            mimetype=file.mimetype,
            file_size=os.path.getsize(file_path)
        )
        db.session.add(new_upload)
        db.session.commit()

        # Parse and validate positions
        positions = request.form.get('positions')
        if positions:
            import json
            positions = json.loads(positions)
            for position in positions:
                if not all(key in position for key in ['line_number', 'description', 'quantity', 'unit_price', 'total_price']):
                    return jsonify({"error": "Invalid position data"}), 400

                new_line_item = LineItem(
                    document_id=new_document.id,
                    line_number=position['line_number'],
                    description=position['description'],
                    quantity=position['quantity'],
                    unit_price=position['unit_price'],
                    total_price=position['total_price'],
                    category_id=parse_uuid_or_none(position.get('category_id')),
                    tax_rate_id=position.get('tax_rate_id'),
                    account_id=parse_uuid_or_none(position.get('account_id'))
                )
                db.session.add(new_line_item)

        db.session.commit()

        return jsonify({"message": "Document, upload, and line items added successfully"}), 201

    except Exception as e:
        db.session.rollback()

        # Lösche die Datei, falls ein Fehler auftritt
        if os.path.exists(file_path):
            os.remove(file_path)

        return jsonify({"error": f"An error occurred while adding new Document: {str(e)}"}), 500


@documents_bp.route('/documents/<uuid:id>', methods=['GET'])
@jwt_required()
def get_document_by_id(id):
    user_id = get_jwt_identity()
    document = Document.query.filter_by(id=id, user_id=user_id).first()

    if not document:
        return jsonify({"error": "Document not found"}), 404

    result = {
        "id": document.id,
        "document_type":document.document_type,
        "status":document.status,
        "number":document.number,
        "document_date":document.document_date,
        "supplier_id":document.supplier_id,
        "delivery_date":document.delivery_date,
        "link_id":document.link_id,
        "due_date":document.due_date,
        "cost_center_id":document.cost_center_id,
        "currency_code":document.currency_code,
    }
    return jsonify(result), 200

@documents_bp.route('/documents/<uuid:id>', methods=['PUT'])
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
        return jsonify({"error": f"Error deleting document and associated data: {str(e)}"}), 500

@documents_bp.route('/documents/<uuid:id>', methods=['DELETE'])
@jwt_required()
def delete_document(id):
    user_id = get_jwt_identity()
    document = Document.query.filter_by(id=id, user_id=user_id).first()
    lineItem = LineItem.query.filter_by(document_id=id).all()
    upload = Upload.query.filter_by(document_id=id).first()

    if not document:
        return jsonify({"error": "Document not found"}), 404

    try:
        for item in lineItem:
            db.session.delete(item)
        db.session.commit()

        if upload and upload.filename:
            # Lösche die Datei vom Server
            file_path = os.path.join(UPLOAD_FOLDER, upload.filename)
            if os.path.exists(file_path):
                os.remove(file_path)

        db.session.delete(upload)
        db.session.commit()

        db.session.delete(document)
        db.session.commit()

        return jsonify({"message": "Document deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
