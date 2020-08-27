[English](https://github.com/yoobool/flask-state/blog/master/master/README.md) | 简体中文

# Flask-State

#### Flask-State是一款基于Flask运行的可视化插件。它能记录每分钟的本机状态以及读取Redis状态（可选项），并通过[Echarts](https://github.com/apache/incubator-echarts)生成数据图表展示给用户。

[![](https://img.shields.io/badge/license-MIT-green.svg?style=flat-square)](https://github.com/yoobool/flask-state/blob/master/LICENSE)


## Installation
#### 安装和更新通过使用 [pip](https://pip.pypa.io/en/stable/quickstart/):
```
$ pip install Flask-State
```


## Usage

#### Flask-State插件安装后，还需要引入JavaScript文件和CSS文件，为你的元素绑定一个约定ID值，即可轻松使用。在某些配置上，你也可以选择修改。

#### 第一步：定义一个Flask app：
```
from flask import Flask
app = flask.Flask(__name__)
```

#### 第二步：调用Flask-State插件的init_app方法初始化相关配置，它将为你添加几条路由用于访问某些配置以及数据库。
```
import flask_state
init_app(app)
```

#### 第三步：在你的html文件中引入相关文件以及为某元素绑定ID值。
```
<link href="http://yoobool.test.upcdn.net/flask_state.css" rel="stylesheet">

# 任意元素:div/button/a/span
<a id='console_machine_status'></a>

<script src="https://cdn.staticfile.org/echarts/4.2.1/echarts.min.js"></script>
<script src="http://yoobool.test.upcdn.net/flask_state.js"></script>
```

#### 额外的：你也可以自定义某些配置文件（非必须）。
```
# 如果你还需要监控REDIS状态，你需要在Flask app上配置你的redis情况
app.config['REDIS_CONF'] = {'REDIS_STATE': True, 'REDIS_HOST': '192.168.1.2', 'REDIS_PORT':16379, 'REDIS_PASSWORD': 'fish09'}
```

```
from flask_state import default_conf_obj

# ID_NAME 为html中绑定元素的id
# 设置为False使用页面元素绑定，True为悬浮球绑定
ID_NAME = (False, 'console_machine_status')
default_conf_obj.set_id_name(ID_NAME)
```

```
from flask_state import default_conf_obj

# LANGUAGE 为插件展示语言，当前有中文，English
LANGUAGE = 'English'
default_conf_obj.set_language(LANGUAGE)
```

```
from flask_state import default_conf_obj

# ADDRESS为数据库名称
# 0为与Flask config同级目录， 1为Flask config的上级目录
ADDRESS = ('console_host', 0)
default_conf_obj.set_address(ADDRESS)
```

```
from flask_state import default_conf_obj

# SECS为记录本机状态时间间隔, 最少间隔为10秒
SECS = 60
default_conf_obj.set_secs(SECS)
```


## Contributing
#### 我们非常欢迎[提出问题](https://github.com/yoobool/flask-state/issues/new)!

#### Flask-State遵循[《贡献者公约》](https://www.contributor-covenant.org/version/1/3/0/code-of-conduct/)行为准则。


## License
#### ......