
from flask import Flask, jsonify, g
from flask_cors import CORS
from flask_login import LoginManager


DEBUG = True
PORT = 8000

import models
from resources.dogs import dogs
from resources.user import user
from resources.veterinarians import veterinarians
from resources.articles import articles
from resources.tips import tips
from dotenv import load_dotenv
import os

load_dotenv(".env")

login_manager = LoginManager()

app = Flask(__name__)

app.secret_key = os.environ.get("App_password")
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    try:
        return models.User.get(models.User.id == user_id)
    except models.DoesNotExist:
        return None

@app.before_request
def before_request():
    """Connect to the database before each request"""
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    """Close the database connection after each request"""
    g.db.close()
    return response

CORS(dogs, origins=['http://localhost:3000'], supports_credentials=True)
app.register_blueprint(dogs, url_prefix='/api/v1/dogs')

CORS(user, origins=['http://localhost:3000'], supports_credentials=True)
app.register_blueprint(user, url_prefix='/api/v1/user')

CORS(veterinarians, origins=['http://localhost:3000'], supports_credentials=True)
app.register_blueprint(veterinarians, url_prefix='/api/v1/veterinarians')

CORS(articles, origins=['http://localhost:3000'], supports_credentials=True)
app.register_blueprint(articles, url_prefix='/api/v1/articles')

CORS(tips, origins=['http://localhost:3000'], supports_credentials=True)
app.register_blueprint(tips, url_prefix='/api/v1/tips')

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)