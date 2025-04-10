from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError

from models import UserChartOfAccountSettings, Account, db

user_chart_of_account_settings_bp = Blueprint('user_chart_of_account_settings_bp', __name__)

@user_chart_of_account_settings_bp.route('/user-chart-of-account-settings', methods=['GET'])
@jwt_required()
def get_user_account_settings():
    """
    Holt alle benutzerspezifischen Konteneinstellungen für den authentifizierten Benutzer.
    """
    current_user_id = get_jwt_identity()

    try:
        settings = UserChartOfAccountSettings.query.filter_by(user_id=current_user_id).all()
        result = []

        for setting in settings:
            account = Account.query.get(setting.account_id)

            if not account:
                continue

            result.append({
                'id': str(setting.id),
                'account_id': str(setting.account_id),
                'account_number': account.number,
                'account_name': account.name,
                'is_active': setting.is_active,
                'custom_name': setting.custom_name,
                'custom_description': setting.custom_description,
                'favorite': setting.favorite
            })

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_chart_of_account_settings_bp.route('/user-chart-of-account-settings/<uuid:account_id>', methods=['GET'])
@jwt_required()
def get_user_account_setting(account_id):
    """
    Holt eine spezifische benutzerspezifische Konteneinstellung.
    """
    current_user_id = get_jwt_identity()

    try:
        setting = UserChartOfAccountSettings.query.filter_by(
            user_id=current_user_id,
            account_id=account_id
        ).first()

        if not setting:
            return jsonify({'error': 'Einstellung nicht gefunden'}), 404

        account = Account.query.get(setting.account_id)

        if not account:
            return jsonify({'error': 'Konto nicht gefunden'}), 404

        result = {
            'id': str(setting.id),
            'account_id': str(setting.account_id),
            'account_number': account.number,
            'account_name': account.name,
            'is_active': setting.is_active,
            'custom_name': setting.custom_name,
            'custom_description': setting.custom_description,
            'favorite': setting.favorite
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_chart_of_account_settings_bp.route('/user-chart-of-account-settings/<uuid:account_id>', methods=['POST'])
@jwt_required()
def create_user_account_setting(account_id):
    """
    Erstellt eine neue benutzerspezifische Konteneinstellung.
    """
    current_user_id = get_jwt_identity()
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Keine Daten erhalten'}), 400

    # Prüfen, ob das Konto existiert
    account = Account.query.get(account_id)
    if not account:
        return jsonify({'error': 'Konto nicht gefunden'}), 404

    # Prüfen, ob bereits eine Einstellung für diesen Benutzer und dieses Konto existiert
    existing_setting = UserChartOfAccountSettings.query.filter_by(
        user_id=current_user_id,
        account_id=account_id
    ).first()

    if existing_setting:
        return jsonify({'error': 'Einstellung existiert bereits'}), 409

    try:
        new_setting = UserChartOfAccountSettings(
            user_id=current_user_id,
            account_id=account_id,
            is_active=data.get('is_active', True),
            custom_name=data.get('custom_name'),
            custom_description=data.get('custom_description'),
            favorite=data.get('favorite', False)
        )

        db.session.add(new_setting)
        db.session.commit()

        result = {
            'id': str(new_setting.id),
            'account_id': str(new_setting.account_id),
            'account_number': account.number,
            'account_name': account.name,
            'is_active': new_setting.is_active,
            'custom_name': new_setting.custom_name,
            'custom_description': new_setting.custom_description,
            'favorite': new_setting.favorite
        }

        return jsonify(result), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Integritätsfehler beim Erstellen der Einstellung'}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_chart_of_account_settings_bp.route('/user-chart-of-account-settings/<uuid:account_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_user_account_setting(account_id):
    """
    Aktualisiert eine bestehende benutzerspezifische Konteneinstellung.
    """
    current_user_id = get_jwt_identity()
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Keine Daten erhalten'}), 400

    try:
        setting = UserChartOfAccountSettings.query.filter_by(
            user_id=current_user_id,
            account_id=account_id
        ).first()

        if not setting:
            return jsonify({'error': 'Einstellung nicht gefunden'}), 404

        # Aktualisieren der Felder, wenn sie in den Daten vorhanden sind
        if 'is_active' in data:
            setting.is_active = data['is_active']

        if 'custom_name' in data:
            setting.custom_name = data['custom_name']

        if 'custom_description' in data:
            setting.custom_description = data['custom_description']

        if 'favorite' in data:
            setting.favorite = data['favorite']

        db.session.commit()

        account = Account.query.get(setting.account_id)

        result = {
            'id': str(setting.id),
            'account_id': str(setting.account_id),
            'account_number': account.number if account else None,
            'account_name': account.name if account else None,
            'is_active': setting.is_active,
            'custom_name': setting.custom_name,
            'custom_description': setting.custom_description,
            'favorite': setting.favorite
        }

        return jsonify(result)

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_chart_of_account_settings_bp.route('/user-chart-of-account-settings/<uuid:account_id>', methods=['DELETE'])
@jwt_required()
def delete_user_account_setting(account_id):
    """
    Löscht eine benutzerspezifische Konteneinstellung.
    """
    current_user_id = get_jwt_identity()

    try:
        setting = UserChartOfAccountSettings.query.filter_by(
            user_id=current_user_id,
            account_id=account_id
        ).first()

        if not setting:
            return jsonify({'error': 'Einstellung nicht gefunden'}), 404

        db.session.delete(setting)
        db.session.commit()

        return jsonify({'message': 'Einstellung erfolgreich gelöscht'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_chart_of_account_settings_bp.route('/user-chart-of-account-settings/favorite', methods=['GET'])
@jwt_required()
def get_favorite_accounts():
    """
    Holt alle als Favorit markierten Konten des Benutzers.
    """
    current_user_id = get_jwt_identity()

    try:
        favorite_settings = UserChartOfAccountSettings.query.filter_by(
            user_id=current_user_id,
            favorite=True
        ).all()

        result = []

        for setting in favorite_settings:
            account = Account.query.get(setting.account_id)

            if not account:
                continue

            result.append({
                'id': str(setting.id),
                'account_id': str(setting.account_id),
                'account_number': account.number,
                'account_name': account.name if not setting.custom_name else setting.custom_name,
                'is_active': setting.is_active,
                'custom_name': setting.custom_name,
                'custom_description': setting.custom_description
            })

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
