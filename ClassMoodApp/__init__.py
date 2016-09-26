from flask import Flask
from ClassMoodApp.Models.DBModels import db
from ClassMoodApp.Config.AppConfig import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)
app.secret_key = '\x1c\x07k5\xfc\x91{\x91x\xd2\\\x81el\xc3\x9d\xee\xed\xdeP\xa1\xda\xcd\xe0'
with app.app_context():
    db.create_all()
from ClassMoodApp.Controllers import *