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
            "steuerart": doc.steuerart
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

    if not file or not description or not category or not beleg_datum or not betrag or not steuerart:
        return jsonify({"error": "All fields are required"}), 400

    # Save the file or process it as needed
    filename = file.filename
    upload_path = f'uploads/{filename}'  # Example path
    file.save(upload_path)

    new_document = Document(
        user_id=user_id,
        filename=filename,
        upload_path=upload_path,
        beleg_datum=beleg_datum,
        betrag=betrag,
        beschreibung=description,
        steuerart=steuerart
    )

    try:
        db.session.add(new_document)
        db.session.commit()
        return jsonify({"message": "Document uploaded successfully", "document_id": str(new_document.id)}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while uploading the document"}), 500
