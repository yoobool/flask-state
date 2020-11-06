[English](https://github.com/yoobool/flask-state/blog/master/master/README.md) | 简体中文

![](https://github.com/yoobool/flask-state/blob/master/src/flask_state/static/flask_state.png)
# Flask-State

Flask-State是一款基于Flask运行的可视化插件。它能记录每分钟的本机状态以及读取Redis状态（可选项），并通过 [Echarts](https://github.com/apache/incubator-echarts) 生成数据图表展示给用户。

[![](https://img.shields.io/badge/Contributions-Welcome-0059b3)](https://github.com/yoobool/flask-state/tree/master/.github/ISSUE_TEMPLATE)
[![](https://img.shields.io/badge/Chat-Gitter-ff69b4.svg?label=Chat&logo=gitter)](https://gitter.im/flaskstate/community)
[![](https://img.shields.io/npm/v/flask-state)](https://www.npmjs.com/package/flask-state)
[![](https://img.shields.io/badge/license-BSD-green)](https://github.com/yoobool/flask-state/blob/master/LICENSE)
[![](https://img.shields.io/badge/python-3.5%20%7C%203.6%20%7C%203.7%20%7C%203.8%20%7C%203.9-blue)](https://pypi.org/project/Flask-State/)

![](https://github.com/yoobool/flask-state/blob/master/examples/static/flask_state.png)


## Installation
安装和更新通过使用 [pip](https://pip.pypa.io/en/stable/quickstart/)
```
$ pip install Flask-State
```

载入显示组件方式可通过标签引入或npm安装
```html
<script src="https://cdn.jsdelivr.net/gh/yoobool/flask-state@v1.0.2/packages/umd/flask-state.min.js"></script>
```
```
npm install flask-state --save
```


## Usage

Flask-State插件安装后，还需要引入JavaScript文件和CSS文件，然后初始化组件运行方式。在某些配置上，你也可以选择修改。

#### 第一步：定义一个Flask app
```python
from flask import Flask
app = Flask(__name__)
```

#### 第二步：绑定数据库地址
```python
from flask_state import DEFAULT_BIND_SQLITE
app.config['SQLALCHEMY_BINDS'] = {DEFAULT_BIND_SQLITE: 'sqlite:///path'}
```

#### 第三步：调用Flask-State插件的init_app方法初始化相关配置，它将为你添加路由用于访问数据库获取本机状态
```python
import flask_state
flask_state.init_app(app)
```

#### 第四步：选择合适的导入方式导入视图文件
```html
<!--cdn方式导入-->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/yoobool/flask-state@v1.0.2/packages/umd/flask-state.css">
<script src="https://cdn.jsdelivr.net/gh/yoobool/flask-state@v1.0.2/packages/umd/flask-state.min.js"></script>
<script type="text/javascript">
    // 创建一个id为'test'的dom节点，init()绑定节点后点击即可打开监听窗口
    flaskState.init({dom:document.getElementById('test')});
</script>
```
```javascript
// npm方式导入
import 'flask-state/flask-state.css';
import {init} from 'flask-state';
// 创建一个id为'test'的dom节点，init()绑定节点后点击即可打开监听窗口
init({dom:document.getElementById('test')});
```

#### 额外的：你也可以自定义某些配置文件（非必须）
如果你还需要监控REDIS状态，你可以在Flask app上配置你的redis地址参数
```python
app.config['REDIS_CONF'] = {'REDIS_STATE': True, 'REDIS_HOST': '192.168.1.3', 'REDIS_PORT':16380, 'REDIS_PASSWORD': 'psw'}
```

修改保存监控记录的时间间隔
```python
# 最少间隔为60秒, 当不设置时间时默认间隔为60秒
import flask_state
SECS = 60
flask_state.init_app(app, SECS)
```

自定义logger对象
```python
import flask_state
import logging
custom_logger = logging.getLogger(__name__)
flask_state.init_app(app, interval=60, log_instance=custom_logger)
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
我们非常欢迎[提出问题](https://github.com/yoobool/flask-state/issues/new)!

Flask-State遵循[《贡献者公约》](https://www.contributor-covenant.org/version/1/3/0/code-of-conduct/) 行为准则。

## Community Channel
我们在 [Gitter](https://gitter.im/flaskstate/community) 等你! 请加入我们.

## License
Flask State使用BSD-3-Clause许可证。