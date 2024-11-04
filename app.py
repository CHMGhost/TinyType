from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash, check_password_hash
from flask_talisman import Talisman
from datetime import datetime
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.tables import TableExtension
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown import markdown
from bleach import clean, linkify
import html
from markupsafe import escape, Markup
import os
from dotenv import load_dotenv
import json
from werkzeug.utils import secure_filename

# Load environment variables
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

# Environment configuration
is_dev = os.getenv('FLASK_ENV', 'development') == 'development'

# Create Flask app
app = Flask(__name__, static_url_path='/static', static_folder='static')

# Configure Flask app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Fetch admin credentials
ADMIN_USERNAME = os.getenv('FLASK_ADMIN_USERNAME')
ADMIN_PASSWORD = os.getenv('FLASK_ADMIN_PASSWORD')
ADMIN_PASSWORD_HASH = generate_password_hash(ADMIN_PASSWORD)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


csp = {
    'default-src': "'self'",
    'img-src': "'self' data:",
    'script-src': [
        "'self'",
        "'unsafe-inline'",
        "'unsafe-eval'",
        "https://cdnjs.cloudflare.com"
    ],
    'style-src': [
        "'self'",
        "'unsafe-inline'",
        "https://cdnjs.cloudflare.com"
    ],
    'font-src': [
        "'self'",
        "https://cdnjs.cloudflare.com",
        "data:"
    ]
}

if is_dev:
    # Development settings - Disable CSP for local development
    Talisman(
        app,
        force_https=False,
        session_cookie_secure=False,
        session_cookie_http_only=True,
        content_security_policy=None,  # Disable CSP in development
        feature_policy=None
    )
else:
    # Production settings - Enable full security
    Talisman(
        app,
        force_https=True,
        session_cookie_secure=True,
        session_cookie_http_only=True,
        content_security_policy=csp,
        content_security_policy_nonce_in=['script-src', 'style-src']
    )

# Add a route to serve static files in development
if is_dev:
    from flask import send_from_directory


    @app.route('/static/<path:filename>')
    def serve_static(filename):
        return send_from_directory('static', filename)

@app.after_request
def add_security_headers(response):
    """Add security headers to each response"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

def secure_render(template_string, **context):
    if not isinstance(template_string, str):
        raise TypeError("Template must be a string")

    escaped_context = {
        k: escape(v) if isinstance(v, str) else v
        for k, v in context.items()
    }

    return render_template(template_string, **escaped_context)


@app.template_filter('markdown')
def markdown_to_html(content):
    """
    Convert markdown to HTML with strict security and no template parsing
    """
    if not content:
        return ''

    # First escape any HTML to prevent injection
    content = html.escape(content)

    # Convert markdown to HTML with specific extensions
    html_content = markdown(
        content,
        extensions=[
            FencedCodeExtension(),
            TableExtension(),
            CodeHiliteExtension(css_class='highlight')
        ]
    )

    # Clean and sanitize HTML
    allowed_tags = [
        'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'ul', 'ol', 'li', 'blockquote', 'pre', 'code',
        'em', 'strong', 'a', 'img', 'table', 'thead', 'tbody',
        'tr', 'th', 'td', 'br', 'hr'
    ]

    allowed_attributes = {
        'a': ['href', 'title', 'rel'],
        'img': ['src', 'alt', 'title'],
        'code': ['class'],
        '*': ['class']
    }

    cleaned_html = clean(
        html_content,
        tags=allowed_tags,
        attributes=allowed_attributes,
        protocols=['http', 'https', 'mailto'],
        strip=True
    )

    # Automatically convert URLs to links
    linked_html = linkify(cleaned_html, parse_email=True)

    return Markup(linked_html)

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

class Draft(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    tags = db.Column(db.Text)  # Store as JSON string
    categories = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

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

    # Use the markdown filter directly
    return render_template(
        'post_detail.html',
        post=post,
        show_return_home=True,
        show_sidebar=True
    )

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload-image', methods=['POST'])
@login_required
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}")
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        return jsonify({'url': url_for('static', filename=f'uploads/{filename}')})

    return jsonify({'error': 'Invalid file type'}), 400


@app.route('/save-draft', methods=['POST'])
@login_required
def save_draft():
    data = request.get_json()

    draft = Draft.query.filter_by(user_id=current_user.id).first()
    if not draft:
        draft = Draft(user_id=current_user.id)

    draft.title = data.get('title', '')
    draft.content = data.get('content', '')
    draft.tags = json.dumps(data.get('tags', []))
    draft.categories = data.get('categories', '')

    db.session.add(draft)
    db.session.commit()

    return jsonify({
        'message': 'Draft saved successfully',
        'updated_at': draft.updated_at.isoformat()
    })


@app.route('/load-draft')
@login_required
def load_draft():
    draft = Draft.query.filter_by(user_id=current_user.id).first()
    if draft:
        return jsonify({
            'draft': {
                'title': draft.title,
                'content': draft.content,
                'tags': json.loads(draft.tags),
                'categories': draft.categories,
                'updated_at': draft.updated_at.isoformat()
            }
        })
    return jsonify({'draft': None})


@app.route('/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()

    if request.method == 'POST':
        # Handle AJAX JSON submission
        if request.is_json:
            data = request.get_json()

            # Create post
            try:
                # Create post
                post = Post(
                    title=data.get('title', '').strip(),
                    content=data.get('content', '').strip(),
                    user_id=current_user.id
                )

                # Handle tags
                if data.get('tags'):
                    for tag_data in json.loads(data['tags']) if isinstance(data['tags'], str) else data['tags']:
                        tag_name = tag_data.get('value', '').strip()
                        if tag_name:
                            tag = Tag.query.filter_by(name=tag_name).first()
                            if not tag:
                                tag = Tag(name=tag_name)
                                db.session.add(tag)
                            post.tags.append(tag)

                # Handle categories
                if data.get('categories'):
                    category_names = [cat.strip() for cat in data['categories'].split(',')]
                    for cat_name in category_names:
                        if cat_name:
                            category = Category.query.filter_by(name=cat_name).first()
                            if not category:
                                category = Category(name=cat_name)
                                db.session.add(category)
                            post.categories.append(category)

                db.session.add(post)

                # Delete draft if exists
                draft = Draft.query.filter_by(user_id=current_user.id).first()
                if draft:
                    db.session.delete(draft)

                db.session.commit()

                return jsonify({
                    'message': 'Post created successfully',
                    'redirect': url_for('post_detail', id=post.id)
                })

            except Exception as e:
                db.session.rollback()
                app.logger.error(f"Error creating post: {str(e)}")
                return jsonify({'errors': {'submit': [str(e)]}}), 500

        # Handle regular form submission
        elif form.validate_on_submit():
            try:
                post = Post(
                    title=form.title.data.strip(),
                    content=form.content.data.strip(),
                    user_id=current_user.id
                )

                # Handle tags
                if form.tags.data:
                    tag_names = [t.strip() for t in form.tags.data.split(',')]
                    for tag_name in tag_names:
                        if tag_name:
                            tag = Tag.query.filter_by(name=tag_name).first()
                            if not tag:
                                tag = Tag(name=tag_name)
                                db.session.add(tag)
                            post.tags.append(tag)

                # Handle categories
                if form.categories.data:
                    category_names = [cat.strip() for cat in form.categories.data.split(',')]
                    for cat_name in category_names:
                        if cat_name:
                            category = Category.query.filter_by(name=cat_name).first()
                            if not category:
                                category = Category(name=cat_name)
                                db.session.add(category)
                            post.categories.append(category)

                db.session.add(post)
                db.session.commit()
                flash('Post created successfully!', 'success')
                return redirect(url_for('home'))

            except Exception as e:
                db.session.rollback()
                app.logger.error(f"Error creating post: {str(e)}")
                flash('Error creating post. Please try again.', 'danger')

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
    query = escape(request.args.get('query', ''))
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

    return render_template(
        'search_results.html',
        posts=posts,
        query=query,
        show_return_home=True,
        show_sidebar=True
    )
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
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', 5000))

    if is_dev:
        # For development with optional SSL
        ssl_context = None
        if os.path.exists('cert.pem') and os.path.exists('key.pem'):
            ssl_context = ('cert.pem', 'key.pem')
        app.run(host=host, port=port, debug=debug_mode, ssl_context=ssl_context)
    else:
        # For production
        app.run(host=host, port=port, debug=False)
