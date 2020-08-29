from setuptools import setup

about = {}
with open("flask_state/__about__.py", "r") as f:
    exec(f.read(), about)

# Metadata goes in setup.cfg. These are here for GitHub's dependency graph.
setup(
    name=about['__title__'],
    version=about['__version__'],
    author="Yoobool",
    url="https://github.com/yoobool/flask-state",
    install_requires=[
        "Werkzeug>=0.15",
        "Jinja2>=2.10.1",
        "itsdangerous>=0.24",
        "click>=5.1",
        "Flask>=1.0",
        "SQLAlchemy>=1.2",
        "Flask-SQLAlchemy>=1.0"
    ]
)
