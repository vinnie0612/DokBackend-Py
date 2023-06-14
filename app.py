from flask import Flask, redirect, render_template, request, session, url_for, jsonify, Response
from flask_session import Session
from datetime import datetime
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
    authority=app.config['MS_AUTHORITY'],
    client_id=app.config['MS_CLIENT_ID'],
    client_credential=app.config['MS_CLIENT_SECRET'])

def login_required(func):
    @wraps(func)
    def login_wrapper(*args, **kwargs):
        if not auth.get_user():
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return login_wrapper

def admin_required(func):
    @wraps(func)
    def admin_wrapper(*args, **kwargs):
        if db.get_user(auth.get_user()['oid']).auth_level < 10:
            return redirect(url_for('index'))
        return func(*args, **kwargs)
    return admin_wrapper

def handle_user_db_sync(user_id,name):
    if not db.get_user_exist(user_id):
        db.create_user(name, user_id)

@app.route('/login')
def login():
    return render_template('login.html', version=app.config['APP_VERSION'], **auth.log_in(
        scopes=app.config['MS_SCOPE'],
        redirect_uri=url_for('auth_response', _external=True),))

@app.route(app.config['MS_AUTH_RESPONSE'])
def auth_response():
    try:
        result = auth.complete_log_in(request.args)
        if 'error' in result:
            return render_template('auth_error.html', result=result)
        user = auth.get_user()
        handle_user_db_sync(user['oid'], user['name'])
        return redirect(url_for('index'))
    except:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    return redirect(auth.log_out(url_for('index', _external=True)))

@app.route('/')
@login_required
def index():
    user=auth.get_user()
    handle_user_db_sync(user['oid'], user['name'])
    return render_template('index.html', user=user, version=app.config['APP_VERSION'], tasks=db.search_tasks_by_user(user['oid']))

@app.route('/door')
@login_required
def door():
    # Open the door somehow
    return 'The door to hell has been opened.'    

@app.route('/userdata')
@login_required
def call_downstream_api():
    token = auth.get_token_for_user(app.config['MS_SCOPE'])
    if 'error' in token:
        return redirect(url_for('login'))
    # Use access token to call downstream api
    api_result = requests.get(
        config.MS_ENDPOINT+'me',
        headers={'Authorization': 'Bearer ' + token['access_token']},
        timeout=30,
    ).json()
    return jsonify(api_result)

@app.route('/pfp')
@login_required
def pfp():
    token = auth.get_token_for_user(app.config['MS_SCOPE'])
    r = requests.get(app.config['MS_ENDPOINT']+'me/photo/$value', headers={'Authorization': 'Bearer ' + token['access_token']})
    headers = {
        'Content-Type': 'image/jpeg',
        'Content-Disposition': 'inline; filename=profile.jpeg'
    }
    return Response(r.content, headers=headers)

@app.route('/admin')
@login_required
@admin_required
def admin():
    user=auth.get_user()
    tasks=db.search_tasks_by_author_id(user["oid"])
    handle_user_db_sync(user['oid'], user['name'])
    return render_template('admin.html',user=user,version=app.config['APP_VERSION'],tasks=tasks)

@app.route('/tasks')
@login_required
def tasks():
    user = auth.get_user()
    tasks = db.search_tasks_by_user(user['oid'])
    task_list = [{'description': task.description, 'deadline': task.deadline, 'author': db.get_user(task.author_id).name, 'task_id': task.task_id} for task in tasks if not task.isdone]
    return jsonify(task_list)

@app.route('/atasks')
@login_required
@admin_required
def atasks():
    user = auth.get_user()
    tasks = db.search_tasks_by_author_id(user['oid'])
    task_list = [{'description': task.description, 'deadline': task.deadline, 'assigned_to': db.get_user(task.assigned_to).name, 'task_id': task.task_id, 'isdone': task.isdone} for task in tasks]
    return jsonify(task_list)

@app.route('/createtask', methods=['POST'])
@login_required
@admin_required
def createtask():
    author_id = auth.get_user()['oid']
    assigned_to = request.form['assigned_to']
    description = request.form['description']
    deadline = datetime.strptime(request.form['deadline'], '%Y-%m-%dT%H:%M')
    task = db.create_task(author_id, assigned_to, description, deadline)
    return redirect(url_for('admin'))

@app.route('/marktaskdone/<task_id>', methods=['GET', 'POST'])
@login_required
def marktaskdone(task_id):
    if request.method == 'GET':
        if db.search_tasks_by_task_id(task_id):
            return render_template('marktaskdone.html', task=db.search_tasks_by_task_id(task_id), user=auth.get_user())
        return "Invalid task!"
    else:
        experience = request.form['experience']
        print(db.add_experience(task_id, experience))
        print(db.mark_task_done(task_id))
        return redirect(url_for('index'))
    
@app.route('/get_users')
@login_required
@admin_required
def get_users():
    users = db.get_all_users()
    user_list = [{'user_id': user.user_id, 'name': user.name} for user in users]
    return jsonify(user_list)

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)