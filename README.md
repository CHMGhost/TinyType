# TinyType

A ridiculously simple blogging engine that gets out of your way. Built with Flask, powered by markdown, and designed to be stupid easy to use.

![TinyType](https://img.shields.io/badge/TinyType-Blogging%20Made%20Tiny-blue)
![Python](https://img.shields.io/badge/Python-3.7+-green)
![License](https://img.shields.io/badge/license-MIT-blue)

## What's This?

TinyType is a no-nonsense blog engine for people who just want to write. No complex dashboards, no endless settings, no nonsense. Just write, publish, and share.

### Why TinyType?
- 🚀 **Stupidly Simple**: Set up in minutes, not hours
- ✍️ **Just Write**: Focus on content with Markdown support
- 🎯 **Zero Bloat**: Only the features you actually need
- 🔒 **Secure Enough**: Basic auth that actually works
- 🎨 **Clean Design**: Minimalist but not boring

## Features

- 📝 Write posts in Markdown
- 🏷️ Organize with tags and categories
- 🔍 Search that actually finds things
- 👤 Simple admin login
- 📱 Mobile-friendly design
- 🎯 Full CRUD operations for posts

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
├── app.py              # The magic happens here
├── blog.db             # Where your posts live
├── static/
│   └── styles.css      # Make it pretty
├── templates/          # The HTML stuff
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   ├── new_post.html
│   ├── edit_post.html
│   ├── post_detail.html
│   ├── posts_by_category.html
│   └── search_results.html
└── requirements.txt    # Python dependencies
```

## Using TinyType

### Writing Posts
1. Log in
2. Hit "New Post"
3. Write stuff (Markdown supported)
4. Add some tags if you want
5. Hit publish

### Markdown Cheatsheet
- `**bold**` → **bold**
- `*italic*` → *italic*
- `# Heading` → Big heading
- `[Link](url)` → [Link]
- ```code``` → For the techies

## Technical Details

### Requirements
```
flask
flask-sqlalchemy
flask-login
flask-wtf
werkzeug
python-dotenv
markdown2
```

### Security Features
- Passwords are hashed (not stored in plaintext like the old days)
- Session management that actually works
- CSRF protection because we care

## Contributing

Found a bug? Want to add something cool or fix something I may have messed up? Here's how:

1. Fork it
2. Branch it (`git checkout -b feature/coolstuff`)
3. Commit it (`git commit -am 'Added some cool stuff'`)
4. Push it (`git push origin feature/coolstuff`)

## License

MIT License - do whatever you want with it (just don't blame us if something breaks).

## Why Another Blog Engine?

Because sometimes you just want something tiny and simple that works. TinyType is for developers who want a blog engine that's:
- Simple enough to understand in one sitting
- Fast enough to deploy in minutes
- Flexible enough to customize without a headache
- Small enough to maintain without a team

Made with ❤️ and probably too much coffee.
