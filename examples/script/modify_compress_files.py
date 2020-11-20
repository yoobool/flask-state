import os

if __name__ == "__main__":
    if os.path.isfile("./packages/main.js"):
        os.remove("./packages/main.js")

    with open("./examples/static/LICENSE", mode="r") as l:
        license_text = l.read()
    l.close()

    with open("./examples/static/initial.js", mode="r", encoding="utf-8") as i:
        content_text = i.readlines()
    i.close()
    content = ""
    for line in content_text:
        content += "    " + line if line.strip() else line

    # cjs
    with open("./packages/cjs/flask-state.js", mode="w", encoding="utf-8") as f:
        cjs_header = "(function () {\n"
        cjs_tail = "})();"
        f.write(license_text + cjs_header + content + "\n" + cjs_tail)
    f.close()

    # cjs.min
    with open("./packages/cjs/flask-state.min.js", mode="r+", encoding="utf-8") as f:
        ori_text = f.read()
        new_text = license_text + ori_text
        f.seek(0)
        f.write(new_text)
    f.close()

    # umd
    with open("./packages/umd/flask-state.js", mode="w", encoding="utf-8") as f:
        umd_header = (
            "(function (global, factory) {\n    typeof exports === 'object' && typeof module !== 'undefined' "
            "? factory(exports) :\n        typeof define === 'function' && define.amd ? define(factory) :\n  "
            "          (factory((global.flaskState = {})));\n}(this, (function (exports) {\n"
        )
        umd_tail = "})));"
        f.write(license_text + umd_header + content + "\n" + umd_tail)
    f.close()

    # umd.min
    with open("./packages/umd/flask-state.min.js", mode="r+", encoding="utf-8") as f:
        ori_text = f.read()
        new_text = license_text + ori_text
        f.seek(0)
        f.write(new_text)
    f.close()
