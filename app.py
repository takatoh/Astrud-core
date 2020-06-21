from bottle import route, static_file, run
import json
from pathlib import Path
from PIL import Image


MimeTypes = {
    ".png" : "image/png",
    ".jpeg" : "image/jpeg",
    ".jpg" : "image/jpeg",
    ".gif" : "image/gif"
}

with open("config.json", "r") as f:
    Config = json.load(f)



@route("/tree")
def tree():
    tree = dir_tree(Config["photoDir"], Config["photoDir"])
    tree["name"] = None
    tree["path"] = ""
    return tree


@route("/dir/<path:path>")
def list_photos(path):
    photo_dir = Config["photoDir"]
    p = Path(photo_dir) / path
    photos = [ str(x.relative_to(photo_dir)) for x in p.iterdir() if x.is_file() ]
    photos.sort()
    dic = { "path" : path, "photos" : photos }
    return dic


@route("/photo/<filepath:path>")
def send_photo(filepath):
    mimetype = MimeTypes[Path(filepath).suffix]
    return static_file(filepath, root=Config["photoDir"], mimetype=mimetype)


# Functions for internal use.

def dir_tree(dir, root):
    p = Path(dir)
    tree = { "name" : str(p.name), "path" : str(p.relative_to(root)) }
    children = [ dir_tree(str(x), root) for x in p.iterdir() if x.is_dir() ]
    children.sort(key=lambda c: c["name"])
    tree["children"] = children
    return tree


def make_thumbnail(photo_path, thumb_path):
    im = Image.open(photo_path)
    im.thumbnail((180, 180))
    im.save()
    return thumb_path



if __name__ == "__main__":
    run(host="localhost", port=8008, debug=True)
