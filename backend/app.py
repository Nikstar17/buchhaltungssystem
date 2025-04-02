from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from config import Config
from models import db
from flask_cors import CORS
from routes.documents_bp import documents_bp
from routes.user_bp import user_bp
from routes.tax_rate_bp import tax_rate_bp
from routes.uploads_bp import uploads_bp
from routes.supplier_bp import supplier_bp
from routes.line_items_bp import line_items_bp


app = Flask(__name__)
CORS(app, origins="http://localhost:5173", supports_credentials=True)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

app.register_blueprint(user_bp)
app.register_blueprint(documents_bp, url_prefix='/api')
app.register_blueprint(tax_rate_bp, url_prefix='/api')
app.register_blueprint(uploads_bp, url_prefix='/api')
app.register_blueprint(supplier_bp, url_prefix='/api')
app.register_blueprint(line_items_bp, url_prefix='/api')

if __name__ == "__main__":
    app.run(debug=True)