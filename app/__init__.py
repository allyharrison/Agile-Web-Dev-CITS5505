from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from .config import Config
from flask_mde import Mde
from flask_moment import Moment
from flask import request
from flask_babel import Babel, lazy_gettext as _l
from elasticsearch import Elasticsearch
from markupsafe import Markup
import re
import bleach

def get_locale():
    return request.accept_languages.best_match(app.config["LANGUAGES"])


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
app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) if app.config['ELASTICSEARCH_URL'] else None

# Define the nl2br custom filter with sanitization and allowed HTML tags/attributes
def nl2br(value):
    if '<' in value and '>' in value:
        # Assume the content is HTML, sanitize it
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol', 'strong', 'ul', 'p', 'br', 'span', 'div']
        allowed_attrs = {
            '*': ['class', 'style'],
            'a': ['href', 'title'],
            'abbr': ['title'],
            'acronym': ['title'],
        }
        clean_value = bleach.clean(value, tags=allowed_tags, attributes=allowed_attrs, strip=True)
        return Markup(clean_value)
    else:
        # Convert newlines to <br> for plain text
        result = re.sub(r'(\r\n|\n\r|\r|\n)', r'<br>', value)
        return Markup(result)

app.jinja_env.filters['nl2br'] = nl2br

print("Elasticsearch URL:", app.config['ELASTICSEARCH_URL'])  # Add this line to debug

from . import routes, models
