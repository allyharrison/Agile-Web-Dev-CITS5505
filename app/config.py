import os # Import the os module for operating system dependent functionality
basedir = os.path.abspath(os.path.dirname(__file__)) # Get the absolute path of the directory containing this file



class Config:
    # Flask configurations
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess' # Set the secret key for session management and CSRF protection
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db') # Set the database URI, defaulting to a local SQLite database if not provided
    # Pagination configuration
    POSTS_PER_PAGE = 5 # Number of posts to display per page
    # Supported languages
    LANGUAGES = ['en'] # List of supported languages for the application
    # Microsoft Translator API key
    MS_TRANSLATOR_KEY = '59be18cdd97f4f6c8578fe1480996bf7'
    # Elasticsearch configuration
    ELASTICSEARCH_URL = 'http://localhost:9200'
    # File upload configuration
    UPLOAD_FOLDER = os.path.join(basedir, 'static/profile_images')
    # Maximum content length for uploads
    MAX_CONTENT_PATH = 16 * 1024 * 1024 