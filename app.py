from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config


app = Flask('app')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_mapping(SQLALCHEMY_DATABASE_URI=config.SQLALCHEMY_DATABASE_URI)
db = SQLAlchemy(app)