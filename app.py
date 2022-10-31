from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm
from sqlalchemy.exc import IntegrityError
# you need this above import sqlalchemy.exc to implement try and catch the error when user is trying to create with the same username

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///flask_feedback_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)
# db.create_all()

toolbar = DebugToolbarExtension(app)

@app.route('/')
def redirect_user():
    """Redirect to /register."""
    return redirect('/register')

# ==============REGISTER/LOGIN/LOGOUT========================#
@app.route('/register', methods=["GET", "POST"] )
def register_user():
    """for "GET" Show a form that when submitted will register/create a user. 
    This form should accept a username, password, email, first_name, and last_name.
    Make sure you are using WTForms and that your password input hides the characters that the user is typing!

    for "POST, Process the registration form by adding a new user. Then redirect to /secret
    """
    form = RegisterForm()

    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        email=form.email.data
        first_name=form.first_name.data
        last_name=form.last_name.data

        # create new user using classmethod "register"
        new_user=User.register(username, password, email, first_name, last_name)

        db.session.add(new_user)
        # handling the error when user picks existing username since username needs to be unique
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append("Username taken. Please pick another")
            return render_template('register.html', form=form)

        session['username'] = new_user.username
        return redirect(f'/users/{new_user.username}')

    
    return render_template('register.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """for "GET", Show a form that when submitted will login a user. This form should accept a username and a password.Make sure you are using WTForms and that your password input hides the characters that the user is typing!

    for "POST", Process the login form, ensuring the user is authenticated and going to "/secret" if so.
    """
    form=LoginForm()

    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data

        user=User.authenticate(username, password)

        if user:
            flash(f"Welcome back, {user.username}!")
            session['username'] =user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors=['Invalid username/password']

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_user():
    session.pop('username')
    flash('goodby', 'info')
    return redirect('/')

# ==============User ROUTE========================#
@app.route('/users/<username>')
def secret(username):
    """Show information about the given user.
    Show all of the feedback that the user has given.

    For each piece of feedback, display with a link to a form to edit the feedback and a button to delete the feedback.

    Have a link that sends you to a form to add more feedback and a button to delete the user Make sure that only the user who is logged in can successfully view this page.
    
    """
    if "username" not in session:
        flash('Please login/register first', 'danger')
        return redirect('/register')

    else:
        user=User.query.get_or_404(username)
        feedbacks = user.feedbacks
        return render_template('user_info.html',user=user, feedbacks=feedbacks)

@app.route('/users/<username>/delete', methods=["POST"])
def delete_user(username):
    """
    Remove the user from the database and make sure to also delete all of their feedback. Clear any user information in the session and redirect to /. Make sure that only the user who is logged in can successfully delete their account
    """
    if "username" not in session:
        flash('You cannot delete this user. Please Login first!', 'danger')
        return redirect('/login')

    else:
        user = User.query.get_or_404(username)
        db.session.delete(user)
        db.session.commit()

        session.pop('username')
        flash(f'Deleted user, {username}', 'success')
        return redirect('/')    
    

# ==============Feedback ROUTE========================#

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedbacck(username):
    """
    for GET, Display a form to add feedback Make sure that only the user who is logged in can see this form

    for POSt, Add a new piece of feedback and redirect to /users/<username> — Make sure that only the user who is logged in can successfully add feedback
    """
    form = FeedbackForm()

    if "username" not in session:
        flash('Please login before adding Feedback!', 'danger')
        return redirect('/')

    if form.validate_on_submit():
        title=form.title.data
        content=form.content.data
        new_feedback = Feedback(title=title, content=content, username=username)
        db.session.add(new_feedback)
        db.session.commit()

        return redirect(f'/users/{username}')

    return render_template("new_feedback.html", form=form)
    

@app.route('/feedback/<feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):
    """
    For GET, Display a form to edit feedback — **Make sure that only the user who has written that feedback can see this form **
    FOR POST, Update a specific piece of feedback and redirect to /users/<username> — Make sure that only the user who has written that feedback can update it
    """
    feedback = Feedback.query.get_or_404(feedback_id)
    form = FeedbackForm(obj=feedback)

    if 'username' not in session:
        flash('Please login before edditing Feedback!', 'danger')
        return redirect('/')

    if form.validate_on_submit():
        feedback.title=form.title.data
        feedback.content=form.content.data

        db.session.commit()

        return redirect(f'/users/{feedback.username}')


    return render_template('edit_feedback.html', form=form)

@app.route('/feedback/<feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    """Delete a specific piece of feedback and redirect to /users/<username> — Make sure that only the user who has written that feedback can delete it"""

    if 'username' not in session:
        flash('Please login before Deleting Feedback!', 'danger')
        return redirect('/login')

    else:
        feedback = Feedback.query.get_or_404(feedback_id)
        db.session.delete(feedback)
        db.session.commit()
        return redirect(f'/users/{feedback.username}')