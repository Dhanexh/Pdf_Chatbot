# app.py
from flask import Flask, session
from flask_cors import CORS
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from models import db
from routes import auth_routes, bot_routes, file_routes
from flask_session import Session

load_dotenv()
os.environ['GOOGLE_API_KEY'] = os.getenv("GOOGLE_API_KEY")
os.environ['SECRET_KEY'] = os.getenv("SECRET_KEY")

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['csv_file'] = 'uploads/pdf'
app.config['ALLOWED_EXTENSIONS'] = {"pdf"}
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = os.getenv("SECRET_KEY")


class Config:
    # Other configurations
    ROLE_PERMISSIONS = {
        'admin': ['upload_file', 'create_bot', 'view_all_bots', 'view_all_users'],
        'user': ['upload_file', 'create_bot', 'view_own_bots'],
    }

# Initialize extensions
CORS(app)
db.init_app(app)
Migrate(app, db)
Session(app)

# Register Blueprints for different functionalities
app.register_blueprint(auth_routes)
app.register_blueprint(bot_routes)
app.register_blueprint(file_routes)

# Create the database if needed
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
