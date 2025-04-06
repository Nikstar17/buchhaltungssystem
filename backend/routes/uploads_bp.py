import os
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import base64

from models import db, Upload, Document

uploads_bp = Blueprint("uploads_bp", __name__)


@uploads_bp.route("/uploads", methods=["POST"])
@jwt_required()
def upload_file():
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({"error": "Benutzer-ID erforderlich"}), 400

    if "file" not in request.files:
        return jsonify({"error": "Keine Datei hochgeladen"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Dateiname fehlt"}), 400

    document_id = request.form.get("document_id")
    if not document_id:
        return jsonify({"error": "Dokument-ID erforderlich"}), 400

    # Dateiinhalt einlesen und Base64-kodieren
    file_content = file.read()
    file_content_base64 = base64.b64encode(file_content).decode("utf-8")
    filename = secure_filename(file.filename)

    # Neuen Upload-Datensatz erstellen mit Base64-Inhalt
    try:
        new_upload = Upload(
            document_id=document_id,
            filename=filename,
            mimetype=file.mimetype,
            file_size=len(file_content),
            file_content=file_content_base64,
        )

        db.session.add(new_upload)
        db.session.commit()

        return (
            jsonify(
                {"message": "Datei erfolgreich hochgeladen", "id": str(new_upload.id)}
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Fehler beim Speichern der Datei: {str(e)}"}), 500


@uploads_bp.route("/uploads/base64/<uuid:document_id>", methods=["GET"])
@jwt_required()
def get_file_base64(document_id):
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({"error": "Benutzer-ID erforderlich"}), 400

    # Prüfe, ob das Dokument zum Benutzer gehört
    document = Document.query.filter_by(id=document_id, user_id=user_id).first()
    if not document:
        return (
            jsonify({"error": "Dokument nicht gefunden oder Zugriff verweigert"}),
            404,
        )

    upload = Upload.query.filter_by(document_id=document_id).first()
    if not upload:
        return jsonify({"error": "Datei nicht gefunden"}), 404

    try:
        # Daten direkt aus der Datenbank zurückgeben
        return (
            jsonify(
                {
                    "file_name": upload.filename,
                    "mimetype": upload.mimetype,
                    "file_data": upload.file_data,
                    "document_id": upload.document_id,
                    "uploaded_at": upload.uploaded_at,
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": f"Fehler beim Abrufen der Datei: {str(e)}"}), 500
