from bottle import route, static_file, hook, response, run, default_app
import json
from pathlib import Path
from PIL import Image


MimeTypes = {
    ".png" : "image/png",
    ".jpeg" : "image/jpeg",
    ".jpg" : "image/jpeg",
    ".gif" : "image/gif"
}

ThumbnailSize = (180, 180)

with open("config.json", "r") as f:
    Config = json.load(f)



@route("/tree")
def tree():
    tree = dir_tree(Path(Config["photoDir"]))
    tree["name"] = "(root)"
    tree["path"] = ""
    return tree


@route("/dir/<path:path>")
def list_photos(path):
    photo_dir = Config["photoDir"]
    p = Path(photo_dir) / path
    make_thumbnails(path)
    photos = [ x.relative_to(photo_dir) for x in p.iterdir() if is_photo(x) ]
    photos = list(map(lambda p: {
        "filename" : p.name,
        "photo" : f"photo/{str(p)}",
        "thumbnail" : f"thumbnail/{str(p.parent / p.stem)}.jpg"
    }, sorted(photos)))
    return { "path" : path, "photos" : photos }


@route("/photo/<filepath:path>")
def send_photo(filepath):
    mimetype = MimeTypes[Path(filepath).suffix]
    return static_file(filepath, root=Config["photoDir"], mimetype=mimetype)


@route("/thumbnail/<filepath:path>")
def send_thumbnail(filepath):
    mimetype = MimeTypes[Path(filepath).suffix]
    return static_file(filepath, root=Config["thumbDir"], mimetype=mimetype)


@hook("after_request")
def enable_cros():
    response.headers["Access-Control-Allow-Origin"] = "*"


# Functions for internal use.

def dir_tree(p):
    tree = {
        "name" : str(p.name),
        "path" : str(p.relative_to(Config["photoDir"])),
        "hasPhotos" : has_photos(p)
    }
    children = [ dir_tree(x) for x in p.iterdir() if x.is_dir() ]
    children.sort(key=lambda c: c["name"])
    tree["children"] = children
    return tree


def has_photos(path):
    for c in path.iterdir():
        if is_photo(c):
            return True
    return False


def make_thumbnail(photo_path, thumb_path):
    if not thumb_path.exists():
        with Image.open(photo_path) as im:
            im.thumbnail(ThumbnailSize)
            im.convert("RGB").save(thumb_path)


def make_thumbnails(dir_path):
    photo_dir = Path(Config["photoDir"]) / dir_path
    thumb_dir = Path(Config["thumbDir"]) / dir_path
    thumb_dir.mkdir(parents=True, exist_ok=True)
    for p in photo_dir.iterdir():
        if is_photo(p):
            make_thumbnail(p, thumb_dir / (p.stem + ".jpg"))


def is_photo(filepath):
    return filepath.is_file() and filepath.suffix in MimeTypes



if __name__ == "__main__":
    run(host="0.0.0.0", port=8008, debug=True)
else:
    application = default_app()
