from flask import Blueprint, request, jsonify
from models import ChartOfAccounts, Account, db
from sqlalchemy.exc import IntegrityError
import uuid

# Create the blueprint
chart_of_account_bp = Blueprint('chart_of_account_bp', __name__)

# Get all chart of accounts
@chart_of_account_bp.route('/chart-of-accounts', methods=['GET'])
def get_all_charts():
    charts = ChartOfAccounts.query.all()
    result = []

    for chart in charts:
        result.append({
            'id': str(chart.id),
            'name': chart.name,
            'description': chart.description,
            'is_standard': chart.is_standard,
            'user_id': str(chart.user_id) if chart.user_id else None
        })

    return jsonify(result)

# Get a specific chart of accounts
@chart_of_account_bp.route('/chart-of-accounts/<uuid:chart_id>', methods=['GET'])
def get_chart(chart_id):
    chart = ChartOfAccounts.query.get_or_404(chart_id)

    result = {
        'id': str(chart.id),
        'name': chart.name,
        'description': chart.description,
        'is_standard': chart.is_standard,
        'user_id': str(chart.user_id) if chart.user_id else None
    }

    return jsonify(result)

# Create a new chart of accounts
@chart_of_account_bp.route('/chart-of-accounts', methods=['POST'])
def create_chart():
    data = request.get_json()

    # Validate required fields
    if not all(key in data for key in ['name']):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        new_chart = ChartOfAccounts(
            name=data['name'],
            description=data.get('description', ''),
            is_standard=data.get('is_standard', False),
            user_id=data.get('user_id')
        )

        db.session.add(new_chart)
        db.session.commit()

        return jsonify({
            'id': str(new_chart.id),
            'message': 'Chart of accounts created successfully'
        }), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Chart of accounts with this name already exists'}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Update a chart of accounts
@chart_of_account_bp.route('/chart-of-accounts/<uuid:chart_id>', methods=['PUT', 'PATCH'])
def update_chart(chart_id):
    chart = ChartOfAccounts.query.get_or_404(chart_id)
    data = request.get_json()

    try:
        if 'name' in data:
            chart.name = data['name']
        if 'description' in data:
            chart.description = data['description']
        if 'is_standard' in data:
            chart.is_standard = data['is_standard']

        db.session.commit()
        return jsonify({'message': 'Chart of accounts updated successfully'})

    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Chart of accounts with this name already exists'}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Delete a chart of accounts
@chart_of_account_bp.route('/chart-of-accounts/<uuid:chart_id>', methods=['DELETE'])
def delete_chart(chart_id):
    chart = ChartOfAccounts.query.get_or_404(chart_id)

    # Don't allow deletion of standard chart of accounts
    if chart.is_standard:
        return jsonify({'error': 'Cannot delete a standard chart of accounts'}), 403

    try:
        db.session.delete(chart)
        db.session.commit()
        return jsonify({'message': 'Chart of accounts deleted successfully'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Get accounts for a specific chart of accounts
@chart_of_account_bp.route('/chart-of-accounts/<uuid:chart_id>/accounts', methods=['GET'])
def get_chart_accounts(chart_id):
    # Verify the chart exists (will return 404 if not found)
    ChartOfAccounts.query.get_or_404(chart_id)

    # Query all accounts for this chart
    accounts = Account.query.filter_by(chart_of_accounts_id=chart_id).all()

    result = []
    for account in accounts:
        account_data = {
        'id': str(account.id),
        'number': account.number,
        'name': account.name,
        'type': str(account.type),
        'active': account.active,
        'description': account.description,
        'account_group': account.account_group,
        'account_class': account.account_class,
        'related_accounts': account.related_accounts  # Hinzugefügt, um die verwandten Konten anzuzeigen
        }
        result.append(account_data)

    return jsonify(result)

