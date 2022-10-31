# Part 1: Create User Model
# First, create a User model for SQLAlchemy. Put this in a models.py file.

# It should have the following columns:

# username - a unique primary key that is no longer than 20 characters.
# password - a not-nullable column that is text
# email - a not-nullable column that is unique and no longer than 50 characters.
# first_name - a not-nullable column that is no longer than 30 characters.
# last_name - a not-nullable column that is no longer than 30 characters.

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

# you need to initialize Bcrypt here
bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):

    __tablename__ = 'users'

    username =db.Column(db.String(20), primary_key=True)
    password =db.Column(db.Text, nullable=False)
    email= db.Column(db.String(50), nullable=False, unique=True)
    first_name= db.Column(db.String(30), nullable=False)
    last_name=db.Column(db.String(30), nullable=False)

    feedbacks = db.relationship('Feedback', backref='user', cascade="all, delete-orphan")

    @classmethod
    def register(cls, username, pwd, email, first_name, last_name):
        hashed_pwd = bcrypt.generate_password_hash(pwd)
        # turn bytestring into normal (unicode utf8) string
        hashed_pwd_utf8 = hashed_pwd.decode('utf8')
        # return instance of user w/username and hashed pwd. it's same thing as writing User(username='tomomi', password='hello') to create new user. instead of "User", you just put "cls" because that's how classmethod is made
        return cls(username=username, password=hashed_pwd_utf8, email=email, first_name=first_name, last_name=last_name) 
    
    @classmethod
    def authenticate(cls, username, pwd):
        """validate that user exists & password is correct.
        retrun user if valid; else return False.
        """
        user=User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, pwd):
            return user
        else:
            return False


class Feedback(db.Model):

    """
    Create a Feedback model for SQLAlchemy. Put this in a models.py file.

    It should have the following columns:

    id - a unique primary key that is an auto incrementing integer
    title - a not-nullable column that is at most 100 characters
    content - a not-nullable column that is text
    username - a foreign key that references the username column in the users table
    """

    __tablename__ ='feedbacks'

    id= db.Column(db.Integer, primary_key=True, autoincrement=True)
    title=db.Column(db.String(100), nullable=False)
    content=db.Column(db.Text, nullable=False)
    username=db.Column(db.String(20), db.ForeignKey('users.username'))

    