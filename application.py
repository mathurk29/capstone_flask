from flask import Flask, app, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField 
from wtforms.validators import DataRequired

# Create a Flask instance
application = Flask(__name__)

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
