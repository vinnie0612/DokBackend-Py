from flask import Flask, redirect, render_template, request, session, url_for, jsonify, Response
from flask_session import Session
from functools import wraps
import db
import requests
import config
import identity.web

app = Flask(__name__)
app.secret_key = config.SECRET_KEY
app.config.from_pyfile('config.py')
Session(app)

# Fixes some stuff when running on localhost
from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

auth = identity.web.Auth(
    session=session,
    authority=app.config["MS_AUTHORITY"],
    client_id=app.config["MS_CLIENT_ID"],
    client_credential=app.config["MS_CLIENT_SECRET"])

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not auth.get_user():
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return wrapper

def handle_user_db_sync(user_id,name):
    if not db.get_user_exist(user_id):
        db.create_user(name, user_id)

@app.route("/login")
def login():
    return render_template("login.html", version=app.config["APP_VERSION"], **auth.log_in(
        scopes=app.config["MS_SCOPE"],
        redirect_uri=url_for("auth_response", _external=True),))

@app.route(app.config["MS_AUTH_RESPONSE"])
def auth_response():
    try:
        result = auth.complete_log_in(request.args)
        if "error" in result:
            return render_template("auth_error.html", result=result)
        user = auth.get_user()
        handle_user_db_sync(user["name"], user["oid"])
        return redirect(url_for("index"))
    except:
        return redirect(url_for('login'))

@app.route("/logout")
def logout():
    return redirect(auth.log_out(url_for("index", _external=True)))

@app.route("/")
@login_required
def index():
    return render_template('index.html', user=auth.get_user(), version=app.config["APP_VERSION"])

@app.route("/door")
@login_required
def door():
    # Open the door somehow
    return "The door to hell has been opened."    

@app.route("/downstream")
@login_required
def call_downstream_api():
    token = auth.get_token_for_user(app.config["MS_SCOPE"])
    if "error" in token:
        return redirect(url_for("login"))
    # Use access token to call downstream api
    api_result = requests.get(
        config.MS_ENDPOINT+"me",
        headers={'Authorization': 'Bearer ' + token['access_token']},
        timeout=30,
    ).json()
    return jsonify(api_result)

@app.route("/pfp")
@login_required
def pfp():
    token = auth.get_token_for_user(app.config["MS_SCOPE"])
    r = requests.get(app.config["MS_ENDPOINT"]+"me/photo/$value", headers={'Authorization': 'Bearer ' + token['access_token']})
    headers = {
        'Content-Type': 'image/jpeg',
        'Content-Disposition': 'inline; filename=profile.jpeg'
    }
    return Response(r.content, headers=headers)

@app.route("/tasks")
@login_required
def tasks():
    user = auth.get_user()
    return db.get_tasks_for_user(user["oid"])

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)