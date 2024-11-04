from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from dotenv import load_dotenv
import markdown2
import json

# Load environment variables
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACvK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Fetch admin credentials from environment variables
ADMIN_USERNAME = os.getenv('FLASK_ADMIN_USERNAME')
ADMIN_PASSWORD = os.getenv('FLASK_ADMIN_PASSWORD')
ADMIN_PASSWORD_HASH = generate_password_hash(ADMIN_PASSWORD)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

post_tags = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

post_categories = db.Table('post_categories',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('posts', lazy=True))
    tags = db.relationship('Tag', secondary=post_tags, lazy='subquery',
        backref=db.backref('posts', lazy=True))
    categories = db.relationship('Category', secondary=post_categories, lazy='subquery',
        backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return '<Post %r>' % self.id


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    tags = StringField('Tags (comma separated)')
    categories = StringField('Categories (comma separated)')
    submit = SubmitField('Submit')


@app.template_filter('markdown')
def markdown_to_html(content):
    return markdown2.markdown(content)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, password):
            user = User.query.filter_by(username=ADMIN_USERNAME).first()
            if user is None:
                user = User(username=ADMIN_USERNAME, password=ADMIN_PASSWORD_HASH)
                db.session.add(user)
                db.session.commit()
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', show_sidebar=False)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/')
def home():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    categories = Category.query.all()
    return render_template('home.html', posts=posts, categories=categories, show_sidebar=True)

@app.route('/category/<int:category_id>')
def posts_by_category(category_id):
    category = Category.query.get_or_404(category_id)
    posts = Post.query.filter(Post.categories.any(id=category.id)).order_by(Post.date_posted.desc()).all()
    categories = Category.query.all()
    return render_template('posts_by_category.html', posts=posts, category=category, categories=categories)


@app.route('/post/<int:id>')
def post_detail(id):
    post = db.session.get(Post, id)
    if post is None:
        return 'Post not found', 404
    post_content_html = markdown2.markdown(post.content)
    return render_template('post_detail.html', post=post, post_content_html=post_content_html, show_return_home=True, show_sidebar=True)


@app.route('/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        tag_names = [tag['value'] for tag in json.loads(request.form['tags'])] if request.form['tags'] else []
        tags = []
        for name in tag_names:
            tag_name = name.strip()
            if tag_name:
                tag = Tag.query.filter_by(name=tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name)
                    db.session.add(tag)
                tags.append(tag)
        category_names = [category.strip() for category in form.categories.data.split(',')] if form.categories.data else []
        categories = []
        for name in category_names:
            if name:
                category = Category.query.filter_by(name=name).first()
                if not category:
                    category = Category(name=name)
                    db.session.add(category)
                categories.append(category)
        new_post = Post(title=title, content=content, user_id=current_user.id, tags=tags, categories=categories)
        try:
            db.session.add(new_post)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(e)
            return 'There was an issue adding your post'
    return render_template('new_post.html', form=form, show_sidebar=False)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = db.session.get(Post, id)
    if post is None:
        return 'Post not found', 404
    if post.user_id != current_user.id:
        flash('You are not authorized to edit this post', 'danger')
        return redirect(url_for('home'))
    form = PostForm(obj=post)
    if request.method == 'GET':
        form.tags.data = ', '.join([tag.name for tag in post.tags])
        form.categories.data = ', '.join([category.name for category in post.categories])
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        tag_names = [tag['value'] for tag in json.loads(request.form['tags'])] if request.form['tags'] else []
        tags = []
        for name in tag_names:
            tag_name = name.strip()
            if tag_name:
                tag = Tag.query.filter_by(name=tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name)
                    db.session.add(tag)
                tags.append(tag)
        category_names = [category.strip() for category in form.categories.data.split(',')] if form.categories.data else []
        categories = []
        for name in category_names:
            if name:
                category = Category.query.filter_by(name=name).first()
                if not category:
                    category = Category(name=name)
                    db.session.add(category)
                categories.append(category)
        post.tags = tags
        post.categories = categories
        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(e)
            return 'There was an issue updating your post'
    return render_template('edit_post.html', form=form, post=post, show_sidebar=False)


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if query:
        search_pattern = f"%{query}%"
        posts = Post.query.filter(
            db.or_(
                Post.title.like(search_pattern),
                Post.content.like(search_pattern),
                Post.tags.any(Tag.name.like(search_pattern)),
                Post.categories.any(Category.name.like(search_pattern))
            )
        ).order_by(Post.date_posted.desc()).all()
    else:
        posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('search_results.html', posts=posts, query=query, show_return_home=True, show_sidebar=True)

@app.route('/delete/<int:id>')
@login_required
def delete_post(id):
    post = db.session.get(Post, id)
    if post is None:
        return 'Post not found', 404
    if post.user_id != current_user.id:
        flash('You are not authorized to delete this post', 'danger')
        return redirect(url_for('home'))
    try:
        db.session.delete(post)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        print(e)
        return 'There was an issue deleting your post'

def init_db():
    if not os.path.exists('blog.db'):
        with app.app_context():
            db.create_all()
            print("Database created successfully.")


if __name__ == '__main__':
    init_db()
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 8000))

    app.run(host=host, port=port, debug=False)

