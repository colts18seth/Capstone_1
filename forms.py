from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
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

class NewQuiz(FlaskForm):
    category = SelectField("Category", choices=[(9, 'General Knowledge'), (10, 'Entertainment: Books'), (11, 'Entertainment: Film'), (12, 'Entertainment: Music'), (13, 'Entertainment: Musicals & Theatres'), (14, 'Entertainment: Television'), (15, 'Entertainment: Video Games'), (16, 'Entertainment: Board Games'), (17, 'Science & Nature'), (18, 'Science: Computers'), (19, 'Science: Mathematics'), (20, 'Mythology'), (21, 'Sports'), (22, 'Geography'), (23, 'History'), (24, 'Politics'), (25, 'Art'), (26, 'Celebrities'), (27, 'Animals'), (28, 'Vehicles'), (29, 'Entertainment: Comics'), (30, 'Science: Gadgets'), (31, 'Entertainment: Japanese Anime &Manga'), (32, 'Entertainment: Cartoon & Animations')])
    num_questions =  SelectField("Number of Questions", choices=[5, 10,15, 20, 25, 30])