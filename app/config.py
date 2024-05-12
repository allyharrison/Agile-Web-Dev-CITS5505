import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    POSTS_PER_PAGE = 5
    LANGUAGES = ['en']
    MS_TRANSLATOR_KEY = '59be18cdd97f4f6c8578fe1480996bf7'
    ELASTICSEARCH_URL = 'http://localhost:9200'