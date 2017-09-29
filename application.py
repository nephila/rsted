#!/usr/bin/env python
# all the imports

import os, sys
try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass

import logging
from flask import Flask, request, render_template, make_response, url_for, jsonify

from rsted.html import rst2html as _rst2html
from rsted.pdf import rst2pdf as _rst2pdf

from flaskext.redis import RedisManager
from flaskext.helpers import render_html

# handle relative path references by changing to project directory
run_from = os.path.dirname(os.path.abspath(__file__))
if run_from != os.path.curdir:
    os.chdir(run_from)

# create our little application :)
app = Flask(__name__)
app.config.from_pyfile(os.environ.get('RSTED_CONF', 'settings.py'))
redis = RedisManager(app).get_instance()

REDIS_EXPIRE = app.config.setdefault('REDIS_EXPIRE', 60*60*24*30*6) # Default 6 months
REDIS_PREFIX = app.config.setdefault('REDIS_PREFIX', 'rst_')
FILES_DIR = app.config.setdefault('FILES_DIR', 'files')


def view_is_active(view_name):
    if request.path == url_for(view_name):
        return 'active'
    return ''

@app.context_processor
def ctx_pro():
    return {
        'MEDIA_URL': '/static/',
        'is_active': view_is_active
    }

@app.route("/")
@render_html('index.html')
def index():
    yield 'js_params', {'theme': request.args.get('theme', '')}

    saved_doc_id = request.args.get('n')
    if saved_doc_id:
        rst = redis.get('%s%s' % (REDIS_PREFIX, saved_doc_id))
        if rst:
            rst = rst.decode('utf-8')
            yield 'rst', rst
            yield 'document', saved_doc_id

@app.route('/srv/rst2html/', methods=['POST', 'GET'])
def rst2html():
    rst = request.form.get('rst', '')
    theme = request.form.get('theme')
    if theme == 'basic':
        theme = None
    try:
        html = _rst2html(rst, theme=theme)
    except Exception as ex:
        html = "<h1>Generation FAILED!</h1>\n<p>%s" % ex
        logging.exception(ex)
    return html

@app.route('/srv/rst2pdf/', methods=['POST'])
def rst2pdf():
    rst = request.form.get('rst', '')
    theme = request.form.get('theme')
    if theme == 'basic':
        theme = None

    pdf = _rst2pdf(rst, theme=theme)
    responce = make_response(pdf)
    responce.headers['Content-Type'] = 'application/pdf'
    responce.headers['Content-Disposition'] = 'attachment; filename="rst.pdf"'
    responce.headers['Content-Transfer-Encoding'] = 'binary'
    return responce

@app.route('/srv/save_rst/', methods=['POST'])
def save_rst():
    rst = request.form.get('rst')
    if not rst:
        return ''

    rst = rst.encode('utf-8')
    from hashlib import md5

    md5sum = md5(rst).hexdigest()
    redis_key = '%s%s' % (REDIS_PREFIX, md5sum)

    if redis.setnx(redis_key, rst) and REDIS_EXPIRE:
        redis.expire(redis_key, REDIS_EXPIRE)
    response = make_response(md5sum)
    response.headers['Content-Type'] = 'text/plain'
    return response

@app.route('/srv/save_file/', methods=['POST'])
def save_file():
    rst = request.form.get('rst')
    project = request.form.get('project')
    filename = request.form.get('filename')
    if not rst:
        return ''
    if not project:
        return ''
    if not filename:
        return ''

    file_path = os.path.join(FILES_DIR, project, filename + '.rst')
    with open(file_path, 'w') as rst_obj:
        rst_obj.write(rst)
    return jsonify(**{'files': get_project_files(project)})

@app.route('/srv/load_file/', methods=['GET'])
def load_file():
    project = request.args.get('project')
    filename = request.args.get('filename')
    if not project:
        return ''
    if not filename:
        return ''

    file_path = os.path.join(FILES_DIR, project, filename + '.rst')
    with open(file_path, 'r') as rst_obj:
        content = rst_obj.read()
    print(file_path, content)
    return jsonify(**{'content': content})

def get_project_files(project):
    project_dir = os.path.join(FILES_DIR, project)
    os.makedirs(project_dir, exist_ok=True)
    content = os.listdir(project_dir)
    return sorted([item[:-4] for item in content if item.endswith('.rst')])

def get_projects():
    os.makedirs(FILES_DIR, exist_ok=True)
    content = os.listdir(FILES_DIR)
    return sorted([item for item in content if os.path.isdir(os.path.join(FILES_DIR, item))])

@app.route('/srv/files/', methods=['GET'])
def files_list():
    project = request.args.get('project')
    if not project:
        return ''

    return jsonify(**{'files': get_project_files(project)})

@app.route('/srv/projects/', methods=['GET'])
def projects():
    return jsonify(**{'projects': get_projects()})

@app.route('/srv/del_rst/', methods=['GET'])
def del_rst():
    saved_id = request.args.get('n')
    if saved_id:
        redis_key = '%s%s' % (REDIS_PREFIX, saved_id)
        redis.delete(redis_key)

    response = make_response()
    response.headers['Content-Type'] = 'text/plain'
    return response

@app.route('/srv/del_file', methods=['POST'])
def del_file():
    project = request.form.get('project')
    filename = request.form.get('filename')
    file_path = os.path.join(FILES_DIR, project, filename + '.rst')
    if file_path:
        try:
            os.remove(file_path)
        except OSError:
            raise

    response = make_response()
    response.headers['Content-Type'] = 'text/plain'
    return response

if __name__ == '__main__':
    app.run(host=app.config.get('HOST', '0.0.0.0'),
            port=app.config.get('PORT', 5000))
