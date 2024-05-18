from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
import sqlalchemy as sa
from app import db
from app.models import User, Comment
from wtforms.validators import DataRequired
from wtforms import TextAreaField
from wtforms.validators import Length
from flask_babel import lazy_gettext as _l
from flask_wtf.file import FileField, FileAllowed


# Form for user login
class LoginForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()],render_kw={"placeholder": "Username"})
    password = PasswordField('Password', validators=[DataRequired()],render_kw={"placeholder": "Password"})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

# Form for user registration
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw={"placeholder": "Enter your username"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Enter your email"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Enter your password"})
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Repeat your password"})
    submit = SubmitField('Register')

    # Custom validation to check if the username already exists
    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(
            User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username.')

    # Custom validation to check if the email already exists
    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(
            User.email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address.')

# Form for editing user profile       
class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    profile_image = FileField('Upload Profile Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
    ])
    submit = SubmitField('Submit')

# Form for creating a post
class PostForm(FlaskForm):
    post = TextAreaField('Say something', validators=[
        DataRequired(), Length(min=1, max=2000)])
    submit = SubmitField('Submit')

# Form with just a submit button, used for actions that don't need other inputs
class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

# Form for sending a message
class MessageForm(FlaskForm):
    message = TextAreaField(_l('Message'), validators=[
        DataRequired(), Length(min=0, max=140)])
    submit = SubmitField(_l('Submit'))  

# Form for adding a comment
class CommentForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired(), Length(min=1, max=1000)])
    submit = SubmitField('Submit')

