![Project Logo](https://cdn.jsdelivr.net/gh/yoobool/flask-state@1.0.5/src/flask_state/static/flask_state.png)

[![Contributor Badge](https://img.shields.io/badge/Contributions-Welcome-0059b3)](https://github.com/yoobool/flask-state/tree/master/.github/ISSUE_TEMPLATE)
[![Gitter Badge](https://img.shields.io/badge/Chat-Gitter-ff69b4.svg?label=Chat&logo=gitter)](https://gitter.im/flaskstate/community)
[![NPM Badge](https://img.shields.io/npm/v/flask-state)](https://www.npmjs.com/package/flask-state)
[![License Badge](https://img.shields.io/badge/license-BSD-green)](https://github.com/yoobool/flask-state/blob/master/LICENSE)
[![Python Badge](https://img.shields.io/badge/python-3.5%20%7C%203.6%20%7C%203.7%20%7C%203.8%20%7C%203.9-blue)](https://pypi.org/project/Flask-State/)

# Flask-State

Flask-State is a lightweight chart plugin for displaying machine state data in your web application.

* **Monitored Metric:** CPU, memory, disk usage, LoadAVG and boot time.
* **Extensible:** Offers rich customization options, including redis monitoring, user authentication,
custom logging, i18n and etc.
* **Stable:** Solves multiprocessing concurrency problems (if you use [gunicorn](https://gunicorn.org/))
built on top of lightweight dependencies.

This project is in active development and thoroughly tested to ensure that Flask-State
stays up-to-date with its project roadmap.

![Screenshot](https://cdn.jsdelivr.net/gh/yoobool/flask-state@1.0.5/examples/static/flask_state.png)

## Documentation

Check out the [live demo](https://flask-state.herokuapp.com/), or head over to the
[tutorial](https://github.com/yoobool/flask-state/wiki/Tutorials) for more instructions.

## Installation

Get this plugin from [PyPI](https://pip.pypa.io/en/stable/quickstart/):

```bash
pip install Flask-State
```

Alternatively, install Flask-State via NPM or include this script tag to the head
section of your HTML document:

```html
<script src="https://cdn.jsdelivr.net/gh/yoobool/flask-state@v1.0.5/packages/umd/flask-state.min.js"></script>
```

```bash
npm install flask-state --save
```

## Usage

### 1. Bind Database Address

```python
from flask_state import DEFAULT_BIND_SQLITE
app.config['SQLALCHEMY_BINDS'] = {DEFAULT_BIND_SQLITE: 'sqlite:///path'}
```

### 2. Configure Flask-State

```python
import flask_state
flask_state.init_app(app)
```

### 3. Include Imports to Views

```javascript
// requires echarts module
import 'echarts';
import 'flask-state/flask-state.min.css';
import {init} from 'flask-state';
// Create a DOM node with ID 'test'. After init() binds the node, 
// click to open the listening window
init({dom:document.getElementById('test')});
```

**Learn more about advanced configurations in the**
[documentation](https://github.com/yoobool/flask-state/wiki/Configuration).

## Contributing

You're welcome to [open a new issue](https://github.com/yoobool/flask-state/issues/new)!
Flask-State follows the [Contributor Covenant](https://www.contributor-covenant.org/version/1/3/0/code-of-conduct/)
Code of Conduct.

## Community Channel

We're on [Gitter](https://gitter.im/flaskstate/community)! Join the conversation
for more questions and inquiries about this project.

## License

Flask-State is available under the BSD-3-Clause License.
