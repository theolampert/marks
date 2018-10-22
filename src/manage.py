import click
import json
import sqlite3


from app import app
from config import DATABASE
from database import create_bookmark, get_bookmarks


@app.cli.command()
def export_json():
    cur = sqlite3.connect(DATABASE).cursor()
    data = json.dumps(get_bookmarks(cur))
    print(data)     # send to stdout


@app.cli.command()
@click.argument('filepath')
def import_json(filepath):
    db = sqlite3.connect(DATABASE)
    file = open(filepath)
    data = json.load(file)

    for bookmark in data:
        create_bookmark(bookmark['url'], bookmark['tags'], db)
