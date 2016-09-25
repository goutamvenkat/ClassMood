from flask import Flask
from ClassMoodApp.Models.DBModels import db
from ClassMoodApp.Config.AppConfig import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)
with app.app_context():
    db.create_all()
from ClassMoodApp.Controllers import *