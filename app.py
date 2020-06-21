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
    tree = dir_tree(Config["photoDir"])
    return json.dumps(tree, indent=2)


def dir_tree(root):
    p = Path(root)
    tree = { "name" : root }
    tree["children"] = [ dir_tree(str(x)) for x in p.iterdir() if x.is_dir() ]
    return tree



run(host="localhost", port=8008, debug=True)
