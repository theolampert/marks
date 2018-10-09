import os
import sqlite3

port = os.getenv('PORT', default=8080)
database = os.getenv('DATABASE', default='example.db')

conn = sqlite3.connect(database)
conn.row_factory = sqlite3.Row
c = conn.cursor()


def bootstrap():
    c.execute('''
        CREATE TABLE tags (
            name text UNIQUE NOT NULL PRIMARY KEY
        )''')
    c.execute('''
        CREATE TABLE urls (
            url text UNIQUE NOT NULL PRIMARY KEY
        )''')
    c.execute('''
        CREATE TABLE tags_urls (
            url text,
            tag text,
            FOREIGN KEY (url) REFERENCES urls(url)
            FOREIGN KEY (tag) REFERENCES tags(name)
        )''')
    conn.commit()


def create_bookmark(url, tags):
    c.execute('INSERT INTO urls (url) VALUES ("{}")'.format(url))
    for tag in tags:
        c.execute('INSERT OR IGNORE INTO tags (name) VALUES ("{}")'.format(tag))
        c.execute('INSERT INTO tags_urls (url, tag) VALUES ("{}", "{}")'.format(url, tag))
    conn.commit()

def get_tags():
    tags = []
    for row in c.execute('SELECT * FROM tags'):
        tags.append(row[0])
    return tags

def get_urls():
    urls = []
    for row in c.execute('SELECT * FROM urls'):
        urls.append(row[0])
    return urls


def get_bookmarks():
    bookmarks = []
    for bookmark in c.execute('''
        SELECT urls.url, GROUP_CONCAT(tags.name, ',') AS tags 
        FROM urls
        JOIN tags_urls ON urls.url = tags_urls.url 
	JOIN tags ON tags_urls.tag = tags.name
        GROUP BY urls.url
    '''):
        bookmarks.append({
            'url': bookmark[0],
            'tags': bookmark[1].split(',')
            })
    return bookmarks

