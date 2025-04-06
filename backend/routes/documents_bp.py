from werkzeug.utils import secure_filename
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Document, Upload, LineItem, Currency, db

ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}  # Erlaubte Dateitypen


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


documents_bp = Blueprint("documents_bp", __name__)


@documents_bp.route("/documents", methods=["GET"])
@jwt_required()
def get_documents():
    user_id = get_jwt_identity()
    documents = Document.query.filter_by(user_id=user_id).all()
    result = [
        {
            "id": str(doc.id),
            "document_number": doc.document_number, # Belegnummer
            "document_type": doc.document_type,     # INCOME / EXPENSE (Ausgang / Eingang)
            "status": doc.status,                   # Status des Belegs
            "supplier_id": doc.supplier_id,         # LieferantID
            "contact_id": doc.contact_id,           # KontaktID
            "issue_date": doc.issue_date,           # Ausstellungsdatum / Belegdatum
            "due_date": doc.due_date,               # Fälligkeitsdatum
            "currency_id": doc.currency_id,         # WährungID
            "is_posted": doc.is_posted,             # Flag für Buchungsstatus
            "created_at": doc.created_at            # Erstelldatum
        }
        for doc in documents
    ]
    return jsonify(result), 200


@documents_bp.route("/documents", methods=["POST"])
@jwt_required()
def set_document():
    user_id = get_jwt_identity()
    data = request.form
    file = request.files.get("file")  # Datei aus dem Request abrufen

    if data is None:
        return jsonify({"error": "Invalid form data"}), 400

    if file is None:
        return jsonify({"error": "Missing file"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed"}), 400

    # Sicheren Dateinamen generieren
    filename = secure_filename(file.filename)

    try:
        # Datei einlesen und Base64-kodieren
        file_content = file.read()
        import base64

        file_content_base64 = base64.b64encode(file_content).decode("utf-8")

        def parse_uuid_or_none(value):
            return value if value not in ("", "null", None) else None

        # Neues Dokument erstellen - angepasst an die Document-Klasse
        new_document = Document(
            user_id=parse_uuid_or_none(user_id),
            document_number=data["number"],  # Belegnummer
            document_type=data["document_type"],  # INCOME / EXPENSE
            status=data["status"],
            supplier_id=parse_uuid_or_none(data["supplier_id"]),
            contact_id=parse_uuid_or_none(data.get("contact_id")),
            issue_date=data["document_date"],  # Ausstellungsdatum / Belegdatum
            due_date=data["due_date"] or None,  # Fälligkeitsdatum
            currency_id=Currency.query.filter_by(code=data.get("currency_code", "EUR"))
            .first()
            .id,
            is_posted=False,  # Standardwert für neue Dokumente
        )

        db.session.add(new_document)
        db.session.commit()

        # Upload-Daten speichern mit Base64-Inhalt
        new_upload = Upload(
            filename=filename,
            mimetype=file.mimetype,
            file_data=file_content_base64,
            document_id=new_document.id,
            user_id=parse_uuid_or_none(user_id),
        )
        db.session.add(new_upload)
        db.session.commit()

        # Parse and validate positions
        positions = request.form.get("positions")
        if positions:
            import json

            positions = json.loads(positions)
            for position in positions:
                if not all(
                    key in position
                    for key in [
                        "line_number",
                        "description",
                        "quantity",
                        "unit_price",
                        "total_price",
                        "category_id",
                        "tax_rate_id"
                    ]
                ):
                    return jsonify({"error": "Invalid position data"}), 400

                new_line_item = LineItem(
                    document_id=new_document.id,
                    line_number=position["line_number"],
                    description=position["description"],
                    quantity=position["quantity"],
                    unit_price=position["unit_price"],
                    total_price=position["total_price"],
                    category_id=parse_uuid_or_none(position.get("category_id")),
                    tax_rate_id=parse_uuid_or_none(position.get("tax_rate_id")),
                )
                db.session.add(new_line_item)

        db.session.commit()

        return (
            jsonify({"message": "Document, upload, and line items added successfully"}),
            201,
        )

    except Exception as e:
        db.session.rollback()
        return (
            jsonify(
                {"error": f"An error occurred while adding new Document: {str(e)}"}
            ),
            500,
        )


@documents_bp.route("/documents/<uuid:id>", methods=["GET"])
@jwt_required()
def get_document_by_id(id):
    user_id = get_jwt_identity()
    doc = Document.query.filter_by(id=id, user_id=user_id).first()

    if not doc:
        return jsonify({"error": "Document not found"}), 404

    result = {
        "id": str(doc.id),
        "document_number": doc.document_number, # Belegnummer
        "document_type": doc.document_type,     # INCOME / EXPENSE (Ausgang / Eingang)
        "status": doc.status,                   # Status des Belegs
        "supplier_id": doc.supplier_id,         # LieferantID
        "contact_id": doc.contact_id,           # KontaktID
        "issue_date": doc.issue_date,           # Ausstellungsdatum / Belegdatum
        "due_date": doc.due_date,               # Fälligkeitsdatum
        "currency_id": doc.currency_id,         # WährungID
        "is_posted": doc.is_posted,             # Flag für Buchungsstatus
        "created_at": doc.created_at            # Erstelldatum
    }
    return jsonify(result), 200


@documents_bp.route("/documents/<uuid:id>", methods=["PUT"])
@jwt_required()
def update_document(id):
    user_id = get_jwt_identity()
    document = Document.query.filter_by(id=id, user_id=user_id).first()

    if not document:
        return jsonify({"error": "Document not found"}), 404

    data = request.json
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400

    beschreibung = data.get("beschreibung")
    kategorie_id = data.get("kategorie_id")
    beleg_datum = data.get("beleg_datum")
    betrag = data.get("betrag")
    steuerart = data.get("steuerart")

    # Validate required fields
    if not beschreibung or not beleg_datum or not betrag or not steuerart:
        return (
            jsonify(
                {
                    "error": "All fields (beschreibung, beleg_datum, betrag, steuerart) are required"
                }
            ),
            400,
        )

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
        return (
            jsonify(
                {"error": f"Error deleting document and associated data: {str(e)}"}
            ),
            500,
        )


@documents_bp.route("/documents/<uuid:id>", methods=["DELETE"])
@jwt_required()
def delete_document(id):
    user_id = get_jwt_identity()
    document = Document.query.filter_by(id=id, user_id=user_id).first()
    lineItem = LineItem.query.filter_by(document_id=id).all()
    upload = Upload.query.filter_by(document_id=id).first()

    if not document:
        return jsonify({"error": "Document not found"}), 404

    try:
        # Lösche LineItems
        for item in lineItem:
            db.session.delete(item)
        db.session.commit()

        # Lösche Upload-Einträge
        if upload:
            db.session.delete(upload)
            db.session.commit()

        # Lösche das Dokument
        db.session.delete(document)
        db.session.commit()

        return jsonify({"message": "Document deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
