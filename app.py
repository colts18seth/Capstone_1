import os

from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from forms import AddUserForm, AddImageForm, LoginForm, NewQuiz
from models import db, connect_db, User, Category, User_Category

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

#export FLASK_ENV=development
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///youGuessedIt'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)
# db.drop_all()
# db.create_all()

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


@app.route("/")
def root():
    return redirect("/signup")


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
            flash("Username already taken!", 'text-danger text-center')
            return render_template('signup.html', form=form)

        login_user(user)

        return redirect(f"/user/{user.id}")

    else:
        return render_template('signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                form.password.data)

        if user:
            login_user(user)
            return redirect(f"/user/{user.id}")

        flash("Invalid credentials.", 'text-danger text-center')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    logout_user()

    return redirect('/login')


##################################################
#User Routes
##################################################

@app.route('/user/<int:user_id>')
def user_details(user_id):
    """Show User Details"""

    user = User.query.get(user_id)

    if user.user_category:
        user_cat = User_Category.query.filter_by(user_id = user.id).all()

        return render_template("user.html", user=user, user_cat=user_cat)
        
    
    return render_template("user.html", user=user)


@app.route('/user/<int:user_id>/edit', methods=["GET", "POST"])
def user_edit(user_id):
    """ Edit User Image """

    form = AddImageForm()

    user = User.query.get(user_id)

    if form.validate_on_submit():
        image = request.form['image_url']
        user.image_url = image

        db.session.commit()

        return redirect(f'/user/{user.id}')

    return render_template('addImage.html', user=user, form=form)


@app.route('/otherUser', methods=['POST'])
def otherUser():
    """ Show otherUser stats """

    user = g.user

    otherU = request.form['search']

    otherUser = User.query.filter_by(username=otherU).one()

    if otherUser.user_category:
        user_cat = User_Category.query.filter_by(user_id = otherUser.id).all()

        return render_template("otherUser.html", otherUser=otherUser, user=user, user_cat=user_cat)

    return render_template('otherUser.html', user=user, otherUser=otherUser)

##################################################
#Quiz Routes
##################################################

@app.route('/quiz', methods=["GET", "POST"])
def quiz():
    """Start New Quiz"""

    if request.method == "POST":
        category_form = request.form['category']
        num_questions = request.form['num_Questions']
        num_correct_answers = request.form['num_correct_answers']

        if Category.query.filter_by(name=category_form).first():
            
            cat = Category.query.filter_by(name=category_form).first()
            user = g.user

            if User_Category.query.filter_by(user_id=user.id, category_id=cat.id).first():
                user_cat = User_Category.query.filter_by(user_id=user.id, category_id=cat.id).first()

                user_cat.quizzes_taken += 1
                user_cat.questions_answered += int(num_questions)
                user_cat.correct_answers += int(num_correct_answers)

                db.session.commit()

            user_cat = User_Category(user_id=user.id, category_id=cat.id, quizzes_taken=1, questions_answered=num_questions, correct_answers=num_correct_answers)
            db.session.add(user_cat)
            db.session.commit()
            

        else:
            category = Category(name=category_form)
            db.session.add(category)
            db.session.commit()

            cat = Category.query.filter_by(name=category_form).first()
            user = g.user

            user_cat = User_Category(user_id=user.id, category_id=cat.id, quizzes_taken=1, questions_answered=num_questions, correct_answers=num_correct_answers)
            db.session.add(user_cat)
            db.session.commit()

        return redirect(f'/user/{user.id}')
    
    form = NewQuiz()

    return render_template('quiz.html', form=form, user=g.user)