import os

from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from forms import AddUserForm, AddImageForm, LoginForm
from models import db, connect_db, User, Category, User_Category

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///youGuessedIt'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)

######################################
#User signup/login/logout
######################################

@app.before_request
def add_user_to_g():
    """ If logged in, add curr user to Flask global. """

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def login_user(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def logout_user():
    """ Logout user. """

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """ Handle user signup. """

    form = AddUserForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                image_url=form.image_url.data or User.image_url.default.arg
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger text-center')
            return render_template('signup.html', form=form)

        login_user(user)

        return redirect("/user")

    else:
        return render_template('signup.html', form=form)

######################
#delete after testing
@app.route("/")
def root():
    return render_template("base.html")

# @app.route('/login', methods=["GET", "POST"])
# def login():
#     """Handle user login."""

#     form = LoginForm()

#     if form.validate_on_submit():
#         user = User.authenticate(form.username.data,
#                                  form.password.data)

#         if user:
#             do_login(user)
#             flash(f"Hello, {user.username}!", 'success  text-center')
#             return redirect("/")

#         flash("Invalid credentials.", 'danger text-center')

#     return render_template('users/login.html', form=form)


# @app.route('/logout')
# def logout():
#     """Handle logout of user."""

#     do_logout()
#     flash('Goodbye!', 'success text-center')

#     return redirect('/login')