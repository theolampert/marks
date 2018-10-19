import os
import sqlite3

from database import create_bookmark, get_bookmarks
from flask import Flask, g, jsonify, request

app = Flask(__name__)
DATABASE = os.getenv('DATABASE', default='example.db')


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.route('/')
def hello_world():
    return 'Hello, world!'


@app.route('/bookmarks')
def all_bookmarks():
    cur = get_db().cursor()
    return jsonify(get_bookmarks(cur))


@app.route('/bookmarks', methods=['POST'])
def post_bookmarks():
    db = get_db()
    cur = db.cursor()
    data = request.get_json()
    create_bookmark(data['url'], data['tags'], cur)
    db.commit()
    return jsonify(data)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
