from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, flash, redirect, render_template, request, url_for
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

class Article(db.Model):
    __table_name__ = "articles"
    id =  db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    content = db.Column(db.String, nullable=False)
    author = db.Column(db.String(), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __repr__(self):
        return f"Article <{self.title}>"

# home page
@app.route('/')
def home():
    articles = Article.query.all()
    return render_template('home.html', articles=articles )

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
        confirm_password = request.form.get('confirmpassword')

        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            return redirect(url_for('login'))

        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            return redirect(url_for('login'))
        if confirm_password != password:
            flash('Password is not equal to confirm password')
            return redirect(url_for('signup'))
        new_user = User(first_name=first_name, last_name=last_name, username=username, email=email, password_hash=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('register.html')

# logout page
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# Individual blog post - /<id_of_blog>
@app.route('/article/<int:_id>')
def single_blog(_id):
    article = Article.query.filter_by(id=_id).first_or_404('Such article does not exist')
    user = User.query.filter_by(username=article.author).first()
    user_id = str(user.id)
    return render_template('singleblog.html', article=article, user_id=user_id, user=user)

# create
@app.route('/create', methods=['POST', 'GET'])
@login_required
def create():
    logged_in_user_id = current_user.get_id() # returns a string so it has to be converted to an integer
    int_of_id = int(logged_in_user_id)
    current_user_object = User.query.filter_by(id=int_of_id).first() # querying the db for the current user details
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        author = current_user_object.username # gets the username of the logged in user

        new_article = Article(title=title, content=content, author=author)
        db.session.add(new_article)
        db.session.commit()
        return redirect(url_for('single_blog', _id=new_article.id))

    return render_template('create.html')

# /<name_of_blog>/edit
@app.route('/article/<int:_id>/edit', methods=['POST', 'GET'])
@login_required
def edit(_id):
    article = Article.query.filter_by(id=_id).first()
    if request.method == 'POST':
        article.content = request.form.get('content')
        article.title = request.form.get('title')
        db.session.commit()
        return redirect(url_for('single_blog', _id=_id))
    return render_template('edit.html', article=article)

# /<name_of_blog>/delete
@app.route('/article/<int:_id>/delete')
@login_required
def delete(_id):
    article = Article.query.filter_by(id=_id).first()
    db.session.delete(article)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)