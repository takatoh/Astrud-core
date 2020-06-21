from bottle import route, run
import json
from pathlib import Path


with open("config.json", "r") as f:
    Config = json.load(f)


@route("/hello")
def hello():
    return "Hello World!"


@route("/config")
def config():
    return json.dumps(Config, indent=2)


@route("/tree")
def tree():
    tree = dir_tree(Config["photoDir"], Config["photoDir"])
    return tree


def dir_tree(dir, root):
    p = Path(dir)
    tree = { "name" : str(p.name), "path" : str(p.relative_to(root)) }
    tree["children"] = [ dir_tree(str(x), root) for x in p.iterdir() if x.is_dir() ]
    return tree



run(host="localhost", port=8008, debug=True)
