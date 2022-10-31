from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email

"""for "GET" Show a form that when submitted will register/create a user. 
This form should accept a username, password, email, first_name, and last_name.
Make sure you are using WTForms and that your password input hides the characters that the user is typing!

for "POST, Process the registration form by adding a new user. Then redirect to /secret
"""

class RegisterForm(FlaskForm):
    username=StringField("Username", validators=[InputRequired()])
    password=PasswordField("Password", validators=[InputRequired()])
    email=StringField("email", validators=[InputRequired(), Email()])
    first_name=StringField("First Name", validators=[InputRequired()])
    last_name=StringField("Last Name", validators=[InputRequired()])


    """for "GET", Show a form that when submitted will login a user. This form should accept a username and a password.Make sure you are using WTForms and that your password input hides the characters that the user is typing!

    for "POST", Process the login form, ensuring the user is authenticated and going to "/secret" if so.
    """

class LoginForm(FlaskForm):
    username=StringField("Username", validators=[InputRequired()])
    password=PasswordField("Password", validators=[InputRequired()])


class FeedbackForm(FlaskForm):
    title=StringField("Title", validators=[InputRequired()])
    content=StringField("Content", validators=[InputRequired()])
   