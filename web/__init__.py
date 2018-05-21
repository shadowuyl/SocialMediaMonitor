from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from configs.config import dbuser,dbpwd
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://'+dbuser+':'+dbpwd+'@localhost:3306/SocialMediaMonitor'
app.config['SECRET_KEY']='H&SvrejwB#e#n05mHYXxIbjNV9lJoWboQGn*oLqm0K5'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['WTF_CSRF_SECRET_KEY']='H&SvrejwB#e#n05mHYXxIbjNV9lJoWboQGn*oLqm0K5'

db = SQLAlchemy(app)

from . import models
from web.views import webapp
