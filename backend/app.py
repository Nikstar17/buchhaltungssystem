from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from config import Config
from models import db
from flask_cors import CORS
from routes.account_bp import account_bp
from routes.booking_bp import booking_bp
from routes.category_bp import category_bp
from routes.documents_bp import documents_bp
from routes.user_bp import user_bp


app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

app.register_blueprint(user_bp)
app.register_blueprint(account_bp, url_prefix='/api')
app.register_blueprint(booking_bp, url_prefix='/api')
app.register_blueprint(category_bp, url_prefix='/api')
app.register_blueprint(documents_bp, url_prefix='/api')

if __name__ == "__main__":
    app.run(debug=True)