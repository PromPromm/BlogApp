from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

base_dir = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///'+ os.path.join(base_dir,'blog.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)

# home page
@app.route('/')
def home():
    return 'home'

# about page
@app.route('/about')
def about():
    return 'about'

# contact page
@app.route('/contact')
def contact():
    return 'contact'

# login page
@app.route('/login')
def login():
    return 'login'

# register page
@app.route('/register')
def signup():
    return 'signup'

# logout page
@app.route('/logout')
def logout():
    return 'logout'

# Individual blog post - /<name_of_blog>
@app.route('/<name_of_blog>')
def single_blog(name_of_blog):
    return 'blog'

# create
@app.route('/create')
def create():
    return 'create'

# /<name_of_blog>/edit
@app.route('/<name_of_blog>/edit')
def edit(name_of_blog):
    return 'edit'
