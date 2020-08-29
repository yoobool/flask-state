from setuptools import setup, find_packages

about = {}
with open('flask_state/__about__.py') as f:
    exec(f.read(), about)
# Metadata goes in setup.cfg. These are here for GitHub's dependency graph.
setup(
    name=about['__title__'],
    version=about['__version__'],
    packages=find_packages(),
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
