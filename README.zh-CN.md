[English](https://github.com/yoobool/flask-state/blob/master/README.md) | 简体中文

![Project Logo](https://cdn.jsdelivr.net/gh/yoobool/flask-state@1.1.1/src/flask_state/static/flask_state.png)

[![Contributor Badge](https://img.shields.io/badge/Contributions-Welcome-0059b3)](https://github.com/yoobool/flask-state/tree/master/.github/ISSUE_TEMPLATE)
[![Gitter Badge](https://img.shields.io/badge/Chat-Gitter-ff69b4.svg?label=Chat&logo=gitter)](https://gitter.im/flaskstate/community)
[![NPM Badge](https://img.shields.io/npm/v/flask-state)](https://www.npmjs.com/package/flask-state)
[![License Badge](https://img.shields.io/badge/license-BSD-green)](https://github.com/yoobool/flask-state/blob/master/LICENSE)
[![Python Badge](https://img.shields.io/badge/python-3.5%20%7C%203.6%20%7C%203.7%20%7C%203.8%20%7C%203.9-blue)](https://pypi.org/project/Flask-State/)

# Flask-State

Flask-State是一款在您浏览器上使用的轻便、图表化插件。

* **监控状态**：CPU，内存，磁盘，磁盘IO, 网络IO, LoadAvg，启动时长。
* **可扩展**：除记录本机状态外，还包括丰富的扩展功能选择。其中有Redis监控、用户验证、自定义logging和i18n等。
* **稳定**：轻量级的依赖关系，同时解决了多进程并发问题。

Flask-State是一个活跃的项目，经过了充分的测试以及有一系列的更新计划。

###

![Screenshot](https://cdn.jsdelivr.net/gh/yoobool/flask-state@1.1.1/examples/static/flask_state.png)

## Documentation

在这里 [live demo](https://flask-state.herokuapp.com/) 可以了解到使用样例, 或者你可以移动到
[tutorial](https://github.com/yoobool/flask-state/wiki/Tutorials) 获取更多信息.

## Installation

从这里 [PyPI](https://pip.pypa.io/en/stable/quickstart/) 下载:

```bash
pip install Flask-State
```

通过NPM安装Flask-State或将此脚本标签放在HTML文件的开头部分:

```html
<script src="https://cdn.jsdelivr.net/gh/yoobool/flask-state@v1.1.1/packages/umd/flask-state.min.js"></script>
<link href="https://cdn.jsdelivr.net/gh/yoobool/flask-state@v1.1.1/packages/flask-state.min.css" rel="stylesheet">
```

```bash
npm install flask-state --save
```

## Usage

Flask-State插件安装后，还需要引入JavaScript文件和CSS文件，然后初始化组件运行方式。在某些配置上，你也可以选择修改。

#### 1. 绑定数据库地址

```python
from flask_state import DEFAULT_BIND_SQLITE
app.config['SQLALCHEMY_BINDS'] = {DEFAULT_BIND_SQLITE: 'sqlite:///path'}
```

#### 2. 配置 Flask-State

```python
import flask_state
flask_state.init_app(app)
```

#### 3. 引入相关模块用于展示

```javascript
// requires echarts module
import 'echarts';
import 'flask-state/flask-state.min.css';
import {init} from 'flask-state';
// Create a DOM node with ID 'test'. After init() binds the node,
// click to open the listening window
init({dom:document.getElementById('test')});
```

**了解更多可配置选项**
[教程](https://github.com/yoobool/flask-state/wiki/Configuration).

## Contributing
[RoadMap](https://github.com/yoobool/flask-state/wiki/Tutorials#roadmap) 中有我们下一步的开发计划.

* [需要其它帮助?](https://www.reddit.com/r/FlaskState/)
* [提出新的问题.](https://github.com/yoobool/flask-state/issues/new)
* [查看其他PR](https://github.com/yoobool/flask-state/pulls).

Flask-State遵循[《贡献者公约》](https://www.contributor-covenant.org/version/1/3/0/code-of-conduct/) 行为准则。

## Alternatives
其他类似的监控开源项目:

* [Flask-MonitoringDashboard](https://github.com/flask-dashboard/Flask-MonitoringDashboard)

## Contributing
我们非常欢迎[提出问题](https://github.com/yoobool/flask-state/issues/new)!

## Community Channel
我们在 [Gitter](https://gitter.im/flaskstate/community) 等你! 请加入我们。

## License
Flask State使用BSD-3-Clause许可证。