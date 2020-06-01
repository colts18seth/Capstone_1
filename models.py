from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """ User in the system """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, default="/static/default-pic.png")
    
    user_category = db.relationship("User_Category", 
                                    backref="user")

    # categories = db.relationship('Category',
    #                             secondary='user_category',
    #                             backref='users')

    def __repr__(self):
        return f"<User #{self.id} - {self.username}>"

    @classmethod
    def signup(cls, username, password, image_url):
        """ Sign up user.  Hash password and add user to system. """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            password=hashed_pwd,
            image_url=image_url
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`. """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class Category(db.Model):
    """ An individual Category """

    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)

    user_category = db.relationship("User_Category", 
                                    backref="category")

    def __repr__(self):
        return f"<Category #{self.id} - {self.name}>"


class User_Category(db.Model):
    """Relates User and Category Models """

    __tablename__ = "user_category"

    user_id = db.Column(db.Integer,
                                        db.ForeignKey("users.id"), primary_key=True)
    category_id = db.Column(db.Integer,
                                        db.ForeignKey("categories.id"), primary_key=True)
    quizzes_taken = db.Column(db.Integer, nullable=False, default=0)
    questions_answered = db.Column(db.Integer, nullable=False,
                                                            default=0)
    correct_answers = db.Column(db.Integer, nullable=False, default=0)
    

    def __repr__(self):
        return f"<User-Category: {self.user_id} - {self.category_id}>"


def connect_db(app):
    """Connect this database to provided Flask app. """

    db.app = app
    db.init_app(app)