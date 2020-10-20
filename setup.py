from setuptools import setup

about = {}
with open('src/flask_state/__about__.py') as f:
    exec(f.read(), about)
# Metadata goes in setup.cfg. These are here for GitHub's dependency graph.
setup(
    name=about['__title__'],
    version=about['__version__'],
    install_requires=[
        "Flask>=1.0",
        "Flask-SQLAlchemy>=1.0",
        "psutil>=5.7.0"
    ]
)
