import os
import time

if __name__ == '__main__':
    try:
        os.remove('./packages/main.js')
    except:
        pass

    # license_text = ''
    with open('./examples/static/LICENSE', mode='r') as f:
        license_text = f.read()

    with open('./packages/cjs/flask-state.js', mode='w+') as f:
        ori_text = f.read()
        new_text = license_text + ori_text
        f.write(ori_text)