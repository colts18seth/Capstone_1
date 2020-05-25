from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length

class AddUserForm(FlaskForm):
    """ Form for adding users """
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[Length(min=6)])
    image_url = StringField("(Optional) Image URL")

class AddImageForm(FlaskForm):
    """ Add image to profile """
    image_url = StringField("Image URL")

class LoginForm(FlaskForm):
    """Login Form """
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[Length(min=6)])