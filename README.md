![](https://github.com/yoobool/flask-state/blob/master/src/flask_state/static/flask_state.png)


[![](https://img.shields.io/badge/Contributions-Welcome-0059b3)](https://github.com/yoobool/flask-state/tree/master/.github/ISSUE_TEMPLATE)
[![](https://img.shields.io/badge/Chat-Gitter-ff69b4.svg?label=Chat&logo=gitter)](https://gitter.im/flaskstate/community)
[![](https://img.shields.io/npm/v/flask-state)](https://www.npmjs.com/package/flask-state)
[![](https://img.shields.io/badge/license-BSD-green)](https://github.com/yoobool/flask-state/blob/master/LICENSE)
[![](https://img.shields.io/badge/python-3.5%20%7C%203.6%20%7C%203.7%20%7C%203.8%20%7C%203.9-blue)](https://pypi.org/project/Flask-State/)

# Flask-State

Flask-State is a visual plug-in based on flask. It can record the local state every minute and read the status of redis if you have configured redis, and generate data chart to show to users through [Echarts](https://github.com/apache/incubator-echarts).

![](https://github.com/yoobool/flask-state/blob/master/examples/static/flask_state.png)

## Installation
Install and update using [pip](https://pip.pypa.io/en/stable/quickstart/):
```
$ pip install Flask-State
```

Display components can use ```<script>``` tag from a CDN, or as a flask-state package on npm.
```html
<script src="https://cdn.jsdelivr.net/gh/yoobool/flask-state@v1.0.2/packages/umd/flask-state.min.js"></script>
```
```
npm install flask-state --save
```


## Usage

After the Flask-State is installed, you also need to import JavaScript file and CSS file to bind a convention ID value for your element. In some configurations, you can also choose to modify them.


### Firstly：we'll set up a Flask app.
```python
from flask import Flask
app = Flask(__name__)
```

### Secondly：Bind database address.
```python
from flask_state import DEFAULT_BIND_SQLITE
app.config['SQLALCHEMY_BINDS'] = {DEFAULT_BIND_SQLITE: 'sqlite:///path'}
```

### Thirdly：Call the init_app method of the flask-state to initialize the configuration.
```python
import flask_state
flask_state.init_app(app)
```

### Lastly：Select the appropriate method to import the view file.
```html
<!--CDN-->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/yoobool/flask-state@v1.0.2/packages/flask-state.css">
<script src="https://cdn.jsdelivr.net/gh/yoobool/flask-state@v1.0.2/packages/umd/flask-state.min.js"></script>
<script type="text/javascript">
    // Create a DOM node with ID 'test'. After init() binds the node, click to open the listening window
    flaskState.init({dom:document.getElementById('test')});
</script>
```
```javascript
// npm
import 'flask-state/flask-state.css';
import {init} from 'flask-state';
// Create a DOM node with ID 'test'. After init() binds the node, click to open the listening window
init({dom:document.getElementById('test')});
```

### Extra：You can also customize some configuration(non-essential).

#### Monitor the redis status.
```python
app.config['REDIS_CONF'] = {'REDIS_STATUS': True, 'REDIS_HOST': '192.168.1.1', 'REDIS_PORT':16380, 'REDIS_PASSWORD': 'psw'}
```

#### Modify the time interval for saving monitoring records.
```python
# The minimum interval is 60 seconds. The default interval is 60 seconds
import flask_state
SECS = 60
flask_state.init_app(app, SECS)
```

#### Custom logger object.
```python
import flask_state
import logging
custom_logger = logging.getLogger(__name__)
flask_state.init_app(app, interval=60, log_instance=custom_logger)
```

#### Custom binding triggers the object of the window.
```javascript
/* When the initialization plug-in does not pass in an object, the plug-in will automatically create a right-hand suspension ball */
/* Note: all pages share a plug-in instance. Calling init() method multiple times will only trigger plug-in events for new object binding */
flaskState.init();
```

#### Select the language in which the plug-in is displayed, now support en, zh.
```html
<!--Note: the language file imported through the tag must be after the plug-in is imported-->
<script src="https://cdn.jsdelivr.net/gh/yoobool/flask-state@v1.0.2/packages/umd/flask-state.min.js"></script>
<script src="https://cdn.jsdelivr.net/gh/yoobool/flask-state@v1.0.2/packages/umd/zh.js"></script>
<script type="text/javascript">
    flaskState.init({lang:flaskState.zh});
</script>
```
```javascript
import {init} from 'flask-state';
import {zh} from 'flask-state/i18n.js';
init({lang:zh});
```


## Contributing
Welcome to [open an issue](https://github.com/yoobool/flask-state/issues/new)!

Flask-State follows the [Contributor Covenant](https://www.contributor-covenant.org/version/1/3/0/code-of-conduct/) Code of Conduct.

## Community Channel
We're on [Gitter](https://gitter.im/flaskstate/community) ! Please join us.

## License
Flask-State is available under the BSD-3-Clause License.