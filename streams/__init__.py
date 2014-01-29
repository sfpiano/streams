from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

app = Flask(__name__)
app.config.from_object('streams.config')
db = SQLAlchemy(app)

lm = LoginManager()
lm.login_view = 'login'
lm.init_app(app)

from streams import views, models
