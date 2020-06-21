from bottle import route, run
import json


with open("config.json", "r") as f:
    Config = json.load(f)


@route("/hello")
def hello():
    return "Hello World!"


@route("/config")
def config():
    return json.dumps(Config, indent=2)


run(host="localhost", port=8008, debug=True)
