from flask import Flask, redirect, request
from tornado.process import task_id

app = Flask(__name__)

from werkzeug.contrib.fixers import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app)

@app.route("/")
def hello():
    cid = task_id()
    cid = "#%s" % cid if cid != None else "MAIN"
    user_ip = request.environ.get("REMOTE_ADDR", "Unknown")
    print "%s: serving a request from %s" % (cid, user_ip)
    return "Hello %s! from %s" % (user_ip, cid)

@app.route("/favicon.ico")
def favicon():
    return redirect("https://www.ep.io/static/images/favicon.ico")

if __name__ == "__main__":
    app.run()
