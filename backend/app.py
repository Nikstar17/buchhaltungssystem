from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from config import Config
from models import db
from flask_cors import CORS

# Import all blueprints
from routes.documents_bp import documents_bp
from routes.user_bp import user_bp
from routes.tax_rate_bp import tax_rate_bp
from routes.uploads_bp import uploads_bp
from routes.supplier_bp import supplier_bp
from routes.line_items_bp import line_items_bp
from routes.chart_of_account_bp import chart_of_account_bp
from routes.user_chart_of_account_settings_bp import user_chart_of_account_settings_bp


app = Flask(__name__)
CORS(app, origins="http://localhost:5173", supports_credentials=True)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# Register all blueprints with the same URL prefix
blueprints = [
    user_bp,
    documents_bp,
    tax_rate_bp,
    uploads_bp,
    supplier_bp,
    line_items_bp,
    chart_of_account_bp,
    user_chart_of_account_settings_bp
]

for blueprint in blueprints:
    app.register_blueprint(blueprint, url_prefix='/api')

if __name__ == "__main__":
    app.run(debug=True)