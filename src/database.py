def bootstrap(cursor):
    cursor.execute('''
        CREATE TABLE if not exists tags (
            name text UNIQUE NOT NULL PRIMARY KEY
        )''')
    cursor.execute('''
        CREATE TABLE if not exists urls (
            url text UNIQUE NOT NULL PRIMARY KEY
        )''')
    cursor.execute('''
        CREATE TABLE if not exists tags_urls (
            url text,
            tag text,
            FOREIGN KEY (url) REFERENCES urls(url)
            FOREIGN KEY (tag) REFERENCES tags(name)
        )''')


def create_bookmark(url, tags, db):
    cursor = db.cursor()
    cursor.execute('INSERT INTO urls (url) VALUES (?)', (url,))
    for tag in tags:
        cursor.execute('INSERT OR IGNORE INTO tags (name) VALUES (?)', (tag,))
        cursor.execute('INSERT INTO tags_urls (url, tag) VALUES (?, ?)', (url, tag,))
    db.commit()


# Just like create but overrides everything
def edit_bookmark(url, tags, db):
    cursor = db.cursor()
    cursor.execute('INSERT OR IGNORE INTO urls (url) VALUES (?)', (url,))
    for tag in tags:
        cursor.execute('INSERT OR IGNORE INTO tags (name) VALUES (?)', (tag,))
        cursor.execute('INSERT OR IGNORE INTO tags_urls (url, tag) VALUES (?, ?)', (url, tag,))
    db.commit()


def delete_bookmark(url, db):
    cursor = db.cursor()
    cursor.execute('DELETE FROM urls WHERE url = ?', (url,))
    cursor.execute('DELETE FROM tags_urls WHERE tags_urls.url = ?', (url,))
    db.commit()


def get_tags(cursor):
    tags = []
    for row in cursor.execute('SELECT * FROM tags'):
        tags.append(row[0])
    return tags


def get_urls(cursor):
    urls = []
    for row in cursor.execute('SELECT * FROM urls'):
        urls.append(row[0])
    return urls


def get_bookmarks(cursor):
    bookmarks = []
    for bookmark in cursor.execute('''
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


def get_bookmarks_with_tag(cursor, tag):
    bookmarks = []
    for bookmark in cursor.execute('''
        SELECT c1.url, GROUP_CONCAT(c2.tag, ',') AS tags
        FROM tags_urls AS c1
        JOIN tags_urls AS c2 ON c1.url = c2.url
        WHERE c1.tag = ?
        GROUP BY c1.url
    ''', (tag,)):
        bookmarks.append({
            'url': bookmark[0],
            'tags': bookmark[1].split(',')
            })
    return bookmarks
