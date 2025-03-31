import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)  # Access-Token läuft nach 15 Minuten ab
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)  # Refresh-Token läuft nach 7 Tagen ab
    JWT_TOKEN_LOCATION = ["cookies"]  # Token wird in Cookies gespeichert
    JWT_COOKIE_SECURE = False  # Nur über HTTPS senden !!!!!!!!!!!!!!!!!!
    JWT_COOKIE_HTTPONLY = True  # Verhindert Zugriff durch JavaScript
    JWT_COOKIE_CSRF_PROTECT = True  # CSRF-Schutz aktivieren
    JWT_CSRF_IN_COOKIES = True  # CSRF-Token in Cookies speichern
    JWT_CSRF_METHODS = ["POST", "PUT", "DELETE"]  # CSRF-Schutz für diese Methoden aktivieren
