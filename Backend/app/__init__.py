from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__, template_folder='../../Frontend/dist', static_folder='../../Frontend/dist/static')
app.config.from_object('config')
CORS(app)

db = SQLAlchemy(app)
db.create_all()

migrate = Migrate(app, db)

from app import views, models
