# TinyType

A ridiculously simple yet secure blogging engine that gets out of your way. Built with Flask, powered by markdown, and designed to be stupid easy to use while maintaining modern security standards.

![TinyType](https://img.shields.io/badge/TinyType-Blogging%20Made%20Tiny-blue)
![Python](https://img.shields.io/badge/Python-3.7+-green)
![License](https://img.shields.io/badge/license-MIT-blue)
![Security](https://img.shields.io/badge/security-enhanced-green)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.2-purple)

## What's This?

TinyType is a no-nonsense blog engine for people who just want to write. No complex dashboards, no endless settings, no nonsense. Just write, publish, and share, all while maintaining modern security practices.

### Why TinyType?
- 🚀 **Stupidly Simple**: Set up in minutes, not hours
- ✍️ **Just Write**: Focus on content with Markdown support
- 🎯 **Zero Bloat**: Only the features you actually need
- 🔒 **Enhanced Security**: Strong security defaults and protections
- 🎨 **Modern Design**: Clean Bootstrap 5 interface with custom styling
- 💾 **Auto-Save**: Never lose your work with automatic draft saving
- 📤 **Image Upload**: Easy image uploading for your posts
- 🔍 **Advanced Search**: Search through posts, tags, and categories
- 📱 **Responsive**: Fully responsive design for all devices

## Features

### Content Management
- 📝 Write posts in Markdown with live preview
- 🏷️ Organize with tags and categories
- 💾 Auto-saving drafts
- 📷 Image upload support
- 🔍 Full-text search across posts, tags, and categories
- 👤 Simple admin login
- 📱 Mobile-friendly design with Bootstrap 5
- 🎯 Full CRUD operations for posts

### Design Features
- 🎨 Modern Bootstrap 5 interface
- 📱 Responsive grid layout
- 🎯 Clean, minimalist design
- 💅 Custom styling with modern CSS
- 🌗 Consistent typography
- 🎨 Beautiful form elements
- 📦 Component-based structure

### Security Features
- 🔐 Content Security Policy (CSP) implementation
- 🛡️ CSRF protection
- 🔑 Secure password hashing
- 🚫 XSS protection
- 📜 Security headers
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
│   ├── styles.css     # Custom styles + Bootstrap overrides
│   └── uploads/       # Image uploads directory
├── templates/         # Jinja2 templates
│   ├── base.html      # Base template with Bootstrap
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

## Styling and Design

### Bootstrap Integration
- Built with Bootstrap 5.3.2
- Custom overrides for unique look
- Responsive grid system
- Modern component library

### Custom Styling
```css
/* Example of our custom styling */
body {
    display: grid;
    grid-template-columns: 250px 1fr;
    grid-template-rows: 100vh;
}

/* Responsive design */
@media (max-width: 768px) {
    body {
        grid-template-columns: 1fr;
        grid-template-rows: auto 1fr;
    }
}
```

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

### Frontend Dependencies
```html
<!-- Bootstrap 5 -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>

<!-- Bootstrap Icons -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css" rel="stylesheet">
```

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
- Beautiful enough out of the box with Bootstrap 5

Made with ❤️ and probably too much coffee.