from bottle import route, run
import json
from pathlib import Path


with open("config.json", "r") as f:
    Config = json.load(f)



@route("/tree")
def tree():
    tree = dir_tree(Config["photoDir"], Config["photoDir"])
    tree["name"] = None
    tree["path"] = ""
    return tree



def dir_tree(dir, root):
    p = Path(dir)
    tree = { "name" : str(p.name), "path" : str(p.relative_to(root)) }
    children = [ dir_tree(str(x), root) for x in p.iterdir() if x.is_dir() ]
    children.sort(key=lambda c: c["name"])
    tree["children"] = children
    return tree



run(host="localhost", port=8008, debug=True)
