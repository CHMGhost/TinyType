# TinyType

A ridiculously simple yet secure blogging engine that gets out of your way. Built with Flask, powered by markdown, and designed to be stupid easy to use while maintaining modern security standards.

![TinyType](https://img.shields.io/badge/TinyType-Blogging%20Made%20Tiny-blue)
![Python](https://img.shields.io/badge/Python-3.7+-green)
![License](https://img.shields.io/badge/license-MIT-blue)
![Security](https://img.shields.io/badge/security-enhanced-green)

## What's This?

TinyType is a no-nonsense blog engine for people who just want to write. No complex dashboards, no endless settings, no nonsense. Just write, publish, and share, all while maintaining modern security practices.

### Why TinyType?
- 🚀 **Stupidly Simple**: Set up in minutes, not hours
- ✍️ **Just Write**: Focus on content with Markdown support
- 🎯 **Zero Bloat**: Only the features you actually need
- 🔒 **Enhanced Security**: Strong security defaults and protections
- 🎨 **Clean Design**: Minimalist but not boring
- 💾 **Auto-Save**: Never lose your work with automatic draft saving
- 📤 **Image Upload**: Easy image uploading for your posts
- 🔍 **Advanced Search**: Search through posts, tags, and categories

## Features

### Content Management
- 📝 Write posts in Markdown with live preview
- 🏷️ Organize with tags and categories
- 💾 Auto-saving drafts
- 📷 Image upload support
- 🔍 Full-text search across posts, tags, and categories
- 👤 Simple admin login
- 📱 Mobile-friendly design
- 🎯 Full CRUD operations for posts

### Security Features
- 🔐 Content Security Policy (CSP) implementation
- 🛡️ CSRF protection
- 🔑 Secure password hashing
- 🚫 XSS protection
- 📜 Security headers (X-Content-Type-Options, X-Frame-Options, etc.)
- 🔒 Secure session management
- 🧹 HTML sanitization for markdown content

## Quick Start

1. Clone it:
```bash
git clone <your-repository-url>
cd tinytype
```

2. Set it up:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
pip install -r requirements.txt
```

3. Configure it:
Create a `.env` file:
```
FLASK_ADMIN_USERNAME=your_admin_username
FLASK_ADMIN_PASSWORD=your_admin_password
SECRET_KEY=your_secret_key
FLASK_ENV=development  # or production
FLASK_DEBUG=False      # True for development
FLASK_HOST=127.0.0.1
FLASK_PORT=5000
```

4. Run it:
```bash
python app.py
```

5. Use it:
- Open `http://localhost:5000`
- Log in and start writing

## Project Structure

```
tinytype/
├── app.py              # Main application logic
├── blog.db            # SQLite database
├── static/
│   ├── styles.css     # Core styles
│   └── uploads/       # Image uploads directory
├── templates/         # Jinja2 templates
│   ├── base.html      # Base template
│   ├── home.html      # Homepage
│   ├── login.html     # Login page
│   ├── new_post.html  # Create post
│   ├── edit_post.html # Edit post
│   ├── post_detail.html # Single post view
│   ├── posts_by_category.html # Category view
│   └── search_results.html # Search results
├── requirements.txt   # Python dependencies
└── tests/            # Test suite
```

## Advanced Features

### Auto-Save Drafts
- Posts are automatically saved as drafts while writing
- Recover your work if your browser crashes
- Draft management system

### Image Upload
- Drag-and-drop image upload support
- Automatic file type validation
- Secure filename handling
- Progress indicator for uploads

### Search Functionality
- Full-text search across posts
- Search within tags and categories
- Real-time search suggestions
- Search result highlighting

### Category Management
- Organize posts by categories
- Category-based navigation
- Category-specific feeds
- Multiple categories per post

## Technical Details

### Requirements
```
Flask>=3.0.3
WTForms>=3.1.2
Werkzeug>=3.0.6
python-dotenv>=1.0.1
Flask-SQLAlchemy>=3.1.1
Flask-Login>=0.6.2
Flask-WTF>=1.2.2
flask-talisman>=1.1.0
Markdown>=3.7
bleach>=6.2.0
```

### Security Implementation
- Content Security Policy (CSP) for preventing XSS attacks
- Secure password hashing using Werkzeug
- CSRF protection using Flask-WTF
- HTML sanitization using Bleach
- Secure file upload handling
- Environment-based security configurations
- Talisman integration for security headers

### Development Mode
- Debug mode configuration
- Optional SSL support in development
- Environment-specific security settings
- Detailed error reporting

## Contributing

Found a bug? Want to add something cool? Here's how:

1. Fork it
2. Branch it (`git checkout -b feature/coolstuff`)
3. Commit it (`git commit -am 'Added some cool stuff'`)
4. Push it (`git push origin feature/coolstuff`)
5. Create a Pull Request

### Testing
Run the test suite:
```bash
pytest basic_test.py
```

## License

MIT License - do whatever you want with it (just don't blame us if something breaks).

## Why Another Blog Engine?

Because sometimes you just want something tiny and simple that works. TinyType is for developers who want a blog engine that's:
- Simple enough to understand in one sitting
- Fast enough to deploy in minutes
- Flexible enough to customize without a headache
- Small enough to maintain without a team
- Secure enough for production use

Made with ❤️ and probably too much coffee.
