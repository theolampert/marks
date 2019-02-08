import sqlite3

from app import app
from config import DATABASE, USERNAME, PASSWORD
from database import (bootstrap, create_bookmark, delete_bookmark,
                      edit_bookmark, get_bookmarks, get_bookmarks_with_tag,
                      get_tags)
from flask import g, jsonify, render_template, request, redirect
from flask_jwt_extended import (
    jwt_required, create_access_token
)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


# Routing
@app.before_first_request
def setup_db():
    print('Bootsraping database')
    db = get_db()
    cur = db.cursor()
    bootstrap(cur)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/auth', methods=['POST'])
def auth():
    username = request.form['username']
    password = request.form['password']

    if username != USERNAME or password != PASSWORD:
        return redirect('/login')

    access_token = create_access_token(identity=username)
    redirect_to_index = redirect('/')
    response = app.make_response(redirect_to_index)
    response.set_cookie('access_token_cookie', value=access_token)
    return response


@app.route('/')
@jwt_required
def index():
    cur = get_db().cursor()
    bookmarks = get_bookmarks(cur)
    return render_template('index.html', bookmarks=bookmarks)


@app.route('/tags')
def all_tags():
    cur = get_db().cursor()
    return jsonify(get_tags(cur))


@app.route('/tags/<tag>')
def get_bookmark_with_tag(tag):
    cur = get_db().cursor()
    bookmarks = get_bookmarks_with_tag(cur, tag)
    return render_template('index.html', bookmarks=bookmarks)


@app.route('/bookmarks')
def all_bookmarks():
    cur = get_db().cursor()
    return jsonify(get_bookmarks(cur))


@app.route('/bookmarks', methods=['POST'])
def post_bookmark():
    db = get_db()
    data = request.get_json()
    create_bookmark(data['url'], data['tags'], db)
    return jsonify(data)


@app.route('/bookmarks', methods=['PUT'])
def put_bookmark():
    db = get_db()
    data = request.get_json()
    edit_bookmark(data['url'], data['tags'], db)
    return jsonify(data)


@app.route('/bookmarks', methods=['DELETE'])
def delete_bookmarks():
    db = get_db()
    data = request.get_json()
    delete_bookmark(data['url'], db)
    return jsonify(data)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
