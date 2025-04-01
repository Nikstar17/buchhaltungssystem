import os
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename

from models import db, Upload

uploads_bp = Blueprint('uploads_bp', __name__)

@uploads_bp.route('/upload', methods=['POST'])
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
            'file_path': f'uploads/{filename}'  # rein informativ
        }), 201

    except Exception as e:
        return jsonify({'error': f'Fehler beim Speichern der Datei: {str(e)}'}), 500