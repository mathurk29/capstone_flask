from datetime import datetime
from enum import unique
from flask import Flask, app, render_template, flash
from flask_wtf import FlaskForm  #wtf is not flask specific - this lib implements it
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# Create a Flask instance
application = Flask(__name__)

# Add database
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# Secret Key
application.config['SECRET_KEY'] = "SOMEKEY"  # for CRF tokens

# Initialize database
db = SQLAlchemy(application)


# Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    # Create a String

    def __repr__(self) -> str:
        return "<Name %r>" % self.name


# User Form
class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Enter button')



# Create a form class
class NamerForm(FlaskForm):
    name = StringField('Enter your name', validators=[DataRequired()])
    submit = SubmitField('Enter button')


@application.route('/user/add', methods=['GET','POST'])
def add_user():
    name=None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash('Users added successfully')
    our_users= Users.query.order_by(Users.date_added)


    return render_template("add_user.html", form=form, name=name, our_users=our_users)


# Create a route decorator
@application.route('/')
# def index():
#     return "<h1>Hello World!</h1>"
def index():
    return render_template("index.html")


# localhost:5000/user/john
@application.route("/user/<username>")
def user(username):
    return render_template('user.html', username=username)


@application.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


# Create Name Page
@application.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form sumitted successfully.")
    return render_template('name.html', name=name, form=form)
