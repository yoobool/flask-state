[English](https://github.com/yoobool/flask-state/blog/master/master/README.md) | 简体中文

# Flask-State

Flask-State是一款基于Flask运行的可视化插件。它能记录每分钟的本机状态以及读取Redis状态（可选项），并通过 [Echarts](https://github.com/apache/incubator-echarts) 生成数据图表展示给用户。

![](https://github.com/yoobool/flask-state/blob/master/examples/static/flask_state.png)

[![](https://img.shields.io/badge/license-BSD-green)](https://github.com/yoobool/flask-state/blob/master/LICENSE)
[![](https://img.shields.io/npm/v/flask-state-test)](https://github.com/yoobool/flask-state/blob/master/LICENSE)
## Installation
安装和更新通过使用 [pip](https://pip.pypa.io/en/stable/quickstart/):
```
$ pip install Flask-State
```

载入显示组件方式可通过标签引入或npm安装
```html
<script src="flask-state-test.js"></script>
```
```
npm install flask-state-test --save
```


## Usage

Flask-State插件安装后，还需要引入JavaScript文件和CSS文件，然后初始化组件运行方式。在某些配置上，你也可以选择修改。

#### 第一步：定义一个Flask app：
```python
from flask import Flask
app = flask.Flask(__name__)
```

#### 第二步：调用Flask-State插件的init_app方法初始化相关配置，它将为你添加几条路由用于访问某些配置以及数据库。
```python
import flask_state
init_app(app)
```

#### 第三步：通过两种不同的安装方式选择适合的导入方式。
```html
<link rel="stylesheet" href="/umd/flask-state.css">
<script src="/umd/flask-state.js"></script>
<script type="text/javascript">
    flaskState.init(document.getElementById('test'));
</script>
```
```javascript
import 'flask-state/flask-state.css';
const flaskState = require('flask-state');
flaskState.init(document.getElementById('test');
```

#### 额外的：你也可以自定义某些配置文件（非必须）。
如果你还需要监控REDIS状态，你可以在Flask app上配置你的redis地址参数
```python
app.config['REDIS_CONF'] = {'REDIS_STATE': True, 'REDIS_HOST': '192.168.1.2', 'REDIS_PORT':16379, 'REDIS_PASSWORD': 'fish09'}
```

将监控记录保存到你指定的数据库地址
```python
from flask_state import flask_state_conf

ADDRESS = 'path/customize.db'
flask_state_conf.set_address(ADDRESS)
```

修改保存监控记录的时间间隔
```python
from flask_state import flask_state_conf

# 最少间隔为10秒
SECS = 60
flask_state_conf.set_secs(SECS)
```

自定义绑定触发窗口的对象
```javascript
/* 初始化插件不传入对象时，插件会自动创建一个右侧悬浮球 */
/* 注意：所有页面共享一个插件实例，多次调用init()方法只会为新的对象绑定触发插件事件 */
flaskState.init();
```

选择插件显示的语言
```html
<!--注意：通过标签导入语言文件必须在导入插件之后-->
<script src="../static/umd/zh.js"></script>
<script type="text/javascript">
    flaskState.init(null, flaskState.zh);
</script>
```
```javascript
import {zh} from 'flask-state/i18n.js';
flaskState.init(null, zh);
```


## Contributing
我们非常欢迎[提出问题](https://github.com/yoobool/flask-state/issues/new)!

Flask-State遵循[《贡献者公约》](https://www.contributor-covenant.org/version/1/3/0/code-of-conduct/) 行为准则。


## License
Flask State使用BSD-3-Clause许可证。