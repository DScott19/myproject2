from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import TextField, TextAreaField, SelectField,StringField,PasswordField
from wtforms.validators import DataRequired, Email,InputRequired

class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    firstname = TextField('First Name', validators=[DataRequired()])
    lastname = TextField('Last Name', validators=[DataRequired()])
    email = TextField('Email', validators=[DataRequired(), Email()])
    location = TextField('Location', validators=[DataRequired()])
    biography=TextAreaField('Biography',validators=[DataRequired()])
    profile_photo = FileField('Profile Picture', validators=[FileRequired(),FileAllowed(['jpg', 'png', 'Images only!'])])



class PostForm(FlaskForm):
    photo = FileField('Photo', validators=[FileRequired(),FileAllowed(['jpg', 'png', 'Images only!'])])
    caption =  TextAreaField('Caption')##no validators because a caption is not a must for a pic
