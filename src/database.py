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


def create_bookmark(url, tags, cursor):
    cursor.execute('INSERT INTO urls (url) VALUES (?)', (url,))
    for tag in tags:
        cursor.execute('INSERT OR IGNORE INTO tags (name) VALUES (?)', (tag,))
        cursor.execute('INSERT INTO tags_urls (url, tag) VALUES (?, ?)', (url, tag,))


def seed(db):
    cursor = db.cursor()
    seeds = [
        {
            'url': 'https://teachyourselfcs.com',
            'tags': [ 'books', 'programming', 'learning' ]
        },
        {
            'url': 'https://xinyminutes.com',
            'tags': [ 'programming', 'reference', 'cheat-sheet' ]
        },
        {
            'url': 'http://protonmail.com',
            'tags': [ 'email', 'privacy' ]
        },
        {
            'url': 'http://github.com/something',
            'tags': [ 'code', 'programming', 'email' ]
        },
        {
            'url': 'http://foobar.com',
            'tags': [ 'fun', 'code' ]
        }
    ]

    for seed in seeds:
        print(seed)
        create_bookmark(seed['url'], seed['tags'], cursor)
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
