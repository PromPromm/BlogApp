from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

base_dir = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///'+ os.path.join(base_dir,'blog.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'b10c5e66032f14ac9208be5d'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"User <{self.username}>"

class Article(db.Model):
    id =  db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    content = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __repr__(self):
        return f"Article <{self.title}>"

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
