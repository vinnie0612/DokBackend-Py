from flask import Flask, redirect, render_template, request, session, url_for, jsonify, Response
from flask_session import Session
from flask_cors import CORS
from datetime import datetime
from functools import wraps
import requests
import config
import identity.web
import importlib
import os
import helpers

# Get the list of files in the "helpers" directory
helpers_dir = os.path.join(os.path.dirname(__file__), 'helpers')
helper_files = os.listdir(helpers_dir)

# Import all the modules from the "helpers" directory
for file in helper_files:
    if file.endswith('.py') and file != '__init__.py':
        module_name = os.path.splitext(file)[0]
        module = importlib.import_module(f'helpers.{module_name}')

        # Add the imported module to the "helpers" namespace
        setattr(helpers, module_name, module)

app = Flask(__name__)
CORS(app)
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
        if helpers.users.get_user(auth.get_user()['oid']).auth_level < 10:
            return redirect(url_for('index'))
        return func(*args, **kwargs)
    return admin_wrapper

def handle_user_db_sync(user_id,name):
    if not helpers.users.get_user_exist(user_id):
        if user_id == app.config['ADMIN_ID']:
            helpers.users.create_user(name, user_id, 10)
        else:
            helpers.users.create_user(name, user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', version=app.config['APP_VERSION'], **auth.log_in(
            scopes=app.config['MS_SCOPE'],
            redirect_uri=url_for('auth_response', _external=True),))
    else:
        auth_uri = auth.log_in(scopes=app.config['MS_SCOPE'],redirect_uri=url_for('auth_response', _external=True))['auth_uri']
        return auth_uri

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

@app.route('/')
@login_required
def index():
    user = auth.get_user()
    handle_user_db_sync(user['oid'], user['name'])
    return render_template('index.html', user=user, version=app.config['APP_VERSION'], tasks=[t for t in helpers.task.search_tasks_by_user(user['oid']) if t.isdone == 0])

@app.route('/doors')
@login_required
def doors():
    raise NotImplementedError("Anyád")

@app.route('/doors/<door>')
def door_open(door):
    raise NotImplementedError("Anyád")

@app.route('/admin')
@login_required
@admin_required
def admin():
    user=auth.get_user()
    tasks=helpers.task.search_tasks_by_author_id(user["oid"])
    handle_user_db_sync(user['oid'], user['name'])
    return render_template('admin.html',user=user,version=app.config['APP_VERSION'],tasks=tasks)

@app.route('/tasks')
@login_required
def tasks():
    user = auth.get_user()
    tasks = helpers.task.search_tasks_by_user(user['oid'])
    task_list = [{'description': t.description, 'deadline': t.deadline, 'author': helpers.users.get_user(t.author_id).name, 'task_id': t.task_id} for t in tasks if not t.isdone]
    return jsonify(task_list)

@app.route('/atasks')
@login_required
@admin_required
def atasks():
    user = auth.get_user()
    tasks = helpers.task.search_tasks_by_author_id(user['oid'])
    task_list = [{'description': t.description, 'deadline': t.deadline, 'assigned_to': helpers.users.get_user(t.assigned_to).name, 'task_id': t.task_id, 'isdone': t.isdone, 'experience': t.experience} for t in tasks]
    return jsonify(task_list)

@app.route('/create_task', methods=['POST'])
@login_required
@admin_required
def createtask():
    author_id = auth.get_user()['oid']
    assigned_to = request.form['assigned_to']
    description = request.form['description']
    deadline = datetime.strptime(request.form['deadline'], '%Y-%m-%dT%H:%M')
    helpers.task.create_task(author_id, assigned_to, description, deadline)
    return redirect(url_for('admin'))

@app.route('/marktaskdone', methods=['POST'])
@login_required
def marktaskdone():
    user = auth.get_user()
    tasks = helpers.task.search_tasks_by_user(user['oid'])
    task_id = request.form['task_id']
    q = [t for t in tasks if t.task_id == task_id]
    task = len(q)
    if task and q[0].isdone == 0:
        helpers.task.mark_task_done(task_id)
        return "OK", 200
    else:
        return "Error", 403
    
@app.route('/add_experience', methods=['POST'])
@login_required
def add_experience():
    user = auth.get_user()
    tasks = helpers.task.search_tasks_by_user(user['oid'])
    task_id = request.form['task_id']
    q = [t for t in tasks if t.task_id == task_id]
    task = len(q)
    if task and q[0].experience == "":
        helpers.task.add_experience(task_id, request.form['experience'])
        return "OK", 200
    else:
        return "Error", 403


@app.route('/get_users')
@login_required
@admin_required
def get_users():
    users = helpers.users.get_all_users()
    user_list = [{'user_id': user.user_id, 'name': user.name} for user in users]
    return jsonify(user_list)

# form should also contain topic, title, content and an image
@app.route('/add_news', methods=['POST'])
@login_required
@admin_required
def add_news():
    author_id = auth.get_user()['oid']
    topic = request.form['topic']
    title = request.form['title']
    content = request.form['content']
    news = helpers.news.create_news(author_id, topic, title, content)
    helpers.image.upload_image(request.files['image'], news.news_id)
    return "OK", 200

@app.route('/del_news', methods=['POST'])
@login_required
@admin_required
def delete_news():
    news_id = request.form['news_id']
    if helpers.news.delete_news(news_id):
        return "OK", 200
    return "Error", 404

@app.route('/news')
def news():
    return helpers.news.get_news()

@app.route('/get_news_image/<news_id>')
def get_news_image(news_id):
    return helpers.image.get_image(news_id)

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)