from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from .config import Config
from flask_mde import Mde
from flask_moment import Moment


app = Flask(__name__)
mde = Mde(app)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
moment = Moment(app)

login = LoginManager(app)
login.login_view = 'login'

from . import routes, models

