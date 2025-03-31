from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Document, db

documents_bp = Blueprint('documents_bp', __name__)

@documents_bp.route('/documents', methods=['GET'])
@jwt_required()
def get_documents():
    user_id = get_jwt_identity()
    documents = Document.query.filter_by(user_id=user_id).all()
    result = [
        {
            "id": str(doc.id),
            "filename": doc.filename,
            "upload_path": doc.upload_path,
            "upload_date": doc.upload_date,
            "beleg_datum": doc.beleg_datum,
            "betrag": float(doc.betrag) if doc.betrag else None,
            "kategorie_id": str(doc.kategorie_id) if doc.kategorie_id else None,
            "beschreibung": doc.beschreibung,
            "steuerart": doc.steuerart,
            "tags": [tag.name for tag in doc.tags]  # Tags hinzufügen
        }
        for doc in documents
    ]
    return jsonify(result), 200

@documents_bp.route('/documents', methods=['POST'])
@jwt_required()
def set_document():
    user_id = get_jwt_identity()

    # Check if a file is included in the request
    if 'file' not in request.files:
        return jsonify({"error": "File is required"}), 400

    file = request.files['file']
    description = request.form.get('description')
    category = request.form.get('category')
    beleg_datum = request.form.get('beleg_datum')
    betrag = request.form.get('betrag')
    steuerart = request.form.get('steuerart')
    tags = request.form.get('tags')  # Kommagetrennte Tags

    if not file or not description or not category or not beleg_datum or not betrag or not steuerart:
        return jsonify({"error": "All fields are required"}), 400

    # Save the file or process it as needed
    filename = file.filename
    upload_path = f'uploads/{filename}'  # Example path
    file.save(upload_path)

    # Beleg erstellen
    new_document = Document(
        user_id=user_id,
        filename=filename,
        upload_path=upload_path,
        beleg_datum=beleg_datum,
        betrag=betrag,
        beschreibung=description,
        steuerart=steuerart
    )

    # Tags verarbeiten
    if tags:
        tag_names = [tag.strip() for tag in tags.split(',')]
        for tag_name in tag_names:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.session.add(tag)
            new_document.tags.append(tag)

    try:
        db.session.add(new_document)
        db.session.commit()
        return jsonify({"message": "Document uploaded successfully", "document_id": str(new_document.id)}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while uploading the document"}), 500

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
