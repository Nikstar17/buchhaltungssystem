import os
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import base64

from models import db, Upload, Document

uploads_bp = Blueprint('uploads_bp', __name__)

@uploads_bp.route('/uploads', methods=['POST'])
@jwt_required()
def upload_file():
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({'error': 'Benutzer-ID erforderlich'}), 400

    if 'file' not in request.files:
        return jsonify({'error': 'Keine Datei hochgeladen'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Dateiname fehlt'}), 400

    filename = secure_filename(file.filename)

    # Absoluter Pfad zu backend/uploads
    current_dir = os.path.dirname(os.path.abspath(__file__))  # backend/routes
    upload_dir = os.path.join(current_dir, '..', 'uploads')
    os.makedirs(upload_dir, exist_ok=True)

    upload_path = os.path.abspath(os.path.join(upload_dir, filename))

    try:
        file.save(upload_path)

        return jsonify({
            'message': 'Datei erfolgreich hochgeladen',
            'file_path': f'uploads/{filename}'
        }), 201

    except Exception as e:
        return jsonify({'error': f'Fehler beim Speichern der Datei: {str(e)}'}), 500

@uploads_bp.route('/uploads/base64/<uuid:document_id>', methods=['GET'])
@jwt_required()
def get_file_base64(document_id):
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({'error': 'Benutzer-ID erforderlich'}), 400

    upload = Upload.query.filter_by(document_id=document_id).first()

    if not upload:
        return jsonify({'error': 'Datei nicht gefunden oder Zugriff verweigert'}), 404

    current_dir = os.path.dirname(os.path.abspath(__file__))  # backend/routes
    upload_dir = os.path.join(current_dir, '..', 'uploads')
    file_path = os.path.abspath(os.path.join(upload_dir, upload.filename))

    if not os.path.exists(file_path):
        return jsonify({'error': 'Datei existiert nicht auf dem Server'}), 404
    try:
        with open(file_path, 'rb') as file:
            file_content = file.read()
            encoded_content = base64.b64encode(file_content).decode('utf-8')
        return jsonify({
            'file_name': upload.filename,
            'file_type': upload.mimetype,
            'content': encoded_content
        }), 200

    except Exception as e:
        return jsonify({'error': f'Fehler beim Abrufen der Datei: {str(e)}'}), 500