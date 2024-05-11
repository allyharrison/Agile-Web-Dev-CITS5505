from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from .config import Config
from flask_mde import Mde
from flask_moment import Moment
from flask import request
from flask_babel import Babel, lazy_gettext as _l


def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])

app = Flask(__name__)
mde = Mde(app)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
moment = Moment(app)
babel = Babel(app, locale_selector=get_locale)

login = LoginManager(app)
login.login_view = 'login'
login.login_message = _l('Please log in to access this page.')



from . import routes, models

