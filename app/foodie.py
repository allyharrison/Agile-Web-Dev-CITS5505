import sqlalchemy as sa
import sqlalchemy.orm as so
from app import app, db
from app.models import User, Post

# Define a shell context processor function 
@app.shell_context_processor
def make_shell_context():
    # Return a dictionary that includes SQLAlchemy core, ORM, database instance, and models
    # This allows these objects to be automatically available in the Flask shell
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Post': Post}
