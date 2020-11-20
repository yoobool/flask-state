![](https://cdn.jsdelivr.net/gh/yoobool/flask-state@1.0.5/src/flask_state/static/flask_state.png)


[![](https://img.shields.io/badge/Contributions-Welcome-0059b3)](https://github.com/yoobool/flask-state/tree/master/.github/ISSUE_TEMPLATE)
[![](https://img.shields.io/badge/Chat-Gitter-ff69b4.svg?label=Chat&logo=gitter)](https://gitter.im/flaskstate/community)
[![](https://img.shields.io/npm/v/flask-state)](https://www.npmjs.com/package/flask-state)
[![](https://img.shields.io/badge/license-BSD-green)](https://github.com/yoobool/flask-state/blob/master/LICENSE)
[![](https://img.shields.io/badge/python-3.5%20%7C%203.6%20%7C%203.7%20%7C%203.8%20%7C%203.9-blue)](https://pypi.org/project/Flask-State/)

# Flask-State

Flask-State is a lightweight chart plugin to show machine state.

* **Monitoring indicators:** CPU, Memory, Disk usage, LoadAVG, Boot time.
* **Extensible:** It has rich options for extended functions, including redis monitoring, user authentication, custom logging, i18n and etc.
* **Stable:** Lightweight dependencies, meanwhile solving multi-progress concurrency problems (if you use [gunicorn](https://gunicorn.org/)).

Flask-State is an active project, well-tested and complete update roadmap.

###

![](https://cdn.jsdelivr.net/gh/yoobool/flask-state@1.0.5/examples/static/flask_state.png)


## Documentation
To check out [live example](https://flask-state.herokuapp.com/), and visit [tutorials doc](https://github.com/yoobool/flask-state/wiki/Tutorials).


## Installation
Install and update using [pip](https://pip.pypa.io/en/stable/quickstart/):
```
$ pip install Flask-State
```

Display components can use ```<script>``` tag from a CDN, or as a flask-state package on npm.
```html
<script src="https://cdn.jsdelivr.net/gh/yoobool/flask-state@v1.0.5/packages/umd/flask-state.min.js"></script>
```
```
npm install flask-state --save
```


## Usage

### Firstly：Bind database address.
```python
from flask_state import DEFAULT_BIND_SQLITE
app.config['SQLALCHEMY_BINDS'] = {DEFAULT_BIND_SQLITE: 'sqlite:///path'}
```

### Secondly：Call the init_app method of the flask-state to initialize the configuration.
```python
import flask_state
flask_state.init_app(app)
```

### Thirdly：Import the view file.
```javascript
// npm
// Need to introduce Echarts module
import 'echarts';
import 'flask-state/flask-state.min.css';
import {init} from 'flask-state';
// Create a DOM node with ID 'test'. After init() binds the node, click to open the listening window
init({dom:document.getElementById('test')});
```

**Learn more about advanced configurations by reading** [documentation](https://github.com/yoobool/flask-state/wiki/Configuration).

## Contributing
Welcome to [open an issue](https://github.com/yoobool/flask-state/issues/new)!

Flask-State follows the [Contributor Covenant](https://www.contributor-covenant.org/version/1/3/0/code-of-conduct/) Code of Conduct.

## Community Channel
We're on [Gitter](https://gitter.im/flaskstate/community) ! Please join us.

## License
Flask-State is available under the BSD-3-Clause License.