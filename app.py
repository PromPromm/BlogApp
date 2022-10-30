from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_user, UserMixin, LoginManager, logout_user, login_required
import os
from datetime import datetime

base_dir = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///'+ os.path.join(base_dir,'blog.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'b10c5e66032f14ac9208be5d'

db = SQLAlchemy(app)
login_manager = LoginManager(app) 

@login_manager.user_loader
def user_loader(id):
    return User.query.get(int(id))

class User(db.Model, UserMixin):
    __table_name__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"User <{self.username}>"

class Article(db.Model, UserMixin):
    __table_name__ = "articles"
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
@app.route('/login', methods=["GET", "POST"])
def login():
        email = request.form.get('email')
        password = request.form.get('password')

        user_exist = User.query.filter_by(email=email).first()
        if user_exist and check_password_hash(user_exist.password_hash, password):
            login_user(user_exist)
            return redirect(url_for('home'))
        return render_template('login.html')

# register page
@app.route('/register', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        first_name = request.form.get('firstname')
        last_name = request.form.get('lastname')
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            return redirect(url_for('login'))

        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            return redirect(url_for('login'))

        new_user = User(first_name=first_name, last_name=last_name, username=username, email=email, password_hash=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html')

# logout page
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

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
