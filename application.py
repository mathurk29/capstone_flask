from flask import Flask, app, render_template

# wtf is not flask specific - the following lib implements it
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField 
from wtforms.validators import DataRequired
from flask import redirect, url_for, request
# Create a Flask instance
application = Flask(__name__)
application.config['SECRET_KEY'] = "SOMEKEY" # for CRF tokens

# Create a form class
class NamerForm(FlaskForm):
    name = StringField('Enter your name', validators=[DataRequired()])
    submit = SubmitField('Enter button')


#Create a route decorator
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
        form.name.data=''
    return render_template('name.html', name=name, form=form)

