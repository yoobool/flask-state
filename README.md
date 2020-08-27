# Flask-State

#### Flask-States is a visual plug-in based on flash. It can record the local state every minute and read redis status (optional)，and generate data chart to show to users through [Echarts](https://github.com/apache/incubator-echarts).

[![](https://img.shields.io/badge/license-MIT-green.svg?style=flat-square)](https://github.com/yoobool/flask-state/blob/master/LICENSE)



## Installation
#### Install and update using [pip](https://pip.pypa.io/en/stable/quickstart/):
```
$ pip install Flask-State
```


## Usage

#### After the Flask-State is installed, you also need to import JavaScript files and CSS files to bind a convention ID value for your element, which can be used easily. In some configurations, you can also choose to modify them.


#### Firstly：we'll set up a Flask app.
```diff
from flask import Flask
app = flask.Flask(__name__)
```

#### Secondly：Call the init_app method of the Flask-State to initialize the relevant configuration. It will add several routes for you to access some configurations and databases.
```
import flask_state
init_app(app)
```

#### Thirdly：Introduce related files into your HTML file and bind ID values for an element.
```
<link href="http://yoobool.test.upcdn.net/flask_state.css" rel="stylesheet">

# Any element: div/button/a/span
<a id='console_machine_status'></a>

<script src="https://cdn.staticfile.org/echarts/4.2.1/echarts.min.js"></script>
<script src="http://yoobool.test.upcdn.net/flask_state.js"></script>
```

#### Extra：You can also customize some configuration files.
```
# If you still need to monitor the redis status, you need to configure your redis status on the Flask app
app.config['REDIS_CONF'] = {'REDIS_STATE': True, 'REDIS_HOST': '192.168.1.2', 'REDIS_PORT':16379, 'REDIS_PASSWORD': 'fish09'}
```

```
from flask_state import default_conf_obj

# ID_NAME is the ID of the binding element in HTML
# Set to false to use page element binding, and true to float ball binding
ID_NAME = (False, 'console_machine_status')
default_conf_obj.set_id_name(ID_NAME)
```

```
from flask_state import default_conf_obj

# LANGUAGE is the plug-in display language, currently there are Chinese，English
LANGUAGE = 'English'
default_conf_obj.set_language(LANGUAGE)
```

```
from flask_state import default_conf_obj

# ADDRESS is the database name
# 0 is the same level directory as Flask config, and 1 is the superior directory of Flask config
ADDRESS = ('console_host', 0)
default_conf_obj.set_address(ADDRESS)
```

```
from flask_state import default_conf_obj

# SECS is the time interval for recording the local state, with a minimum interval of 10 seconds
SECS = 60
default_conf_obj.set_secs(SECS)
```



## Contributing
#### Welcome to [open an issue](https://github.com/yoobool/flask-state/issues/new)!

#### Flask-State follows the [Contributor Covenant](https://www.contributor-covenant.org/version/1/3/0/code-of-conduct/) Code of Conduct.


## License
#### ......