# Flask-State
## Usage Examples HOW TO

### First time setup
Clone `Flask-State` locally, or download the `examples` directory
```shell script
git clone https://github.com/yoobool/flask-state.git
cd flask-state
```

### Install Python Packages
You can create a virtualenv before install package optionally.
```shell script
python3 -m venv env
. env/bin/activate
```
Install packages for `examples`
```shell script
pip install "flask-state[full]"
```

### Install Redis
You can install through Redis binary release, Ubuntu PPA,<br>
build from source or via Docker.

For more info, check out [Redis - Download](https://redis.io/download)
, Remember to change config in `examples/config.py` after install.

If you have `docker-compose`, you can also create a redis container simply via:
```shell script
# cd path/to/flask-state/examples
docker-compose up -d
```

### Done!
Run examples app via:
```shell script
# cd path/to/flask-state/examples
python3 app.py
```
Checkout pages on your [browser](http://127.0.0.1:5000)
```shell script
http://127.0.0.1:5000
```