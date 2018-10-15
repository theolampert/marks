import os
import unittest
from database import bootstrap, create_bookmark, get_bookmarks

import sqlite3


DATABASE = os.getenv('DATABASE', default='__test.db')
conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

class TestBookmarks(unittest.TestCase):
    def setUp(self):
        bootstrap(cursor)

    def test_create(self):
        url = 'https://foobar.com'
        tags = ['foo', 'bar']

        create_bookmark(url, tags, cursor)
        conn.commit()
        bookmarks = get_bookmarks(cursor)
        bookmark = bookmarks[0]

        self.assertEqual(len(bookmarks), 1)
        self.assertEqual(bookmark['url'], url)
        self.assertEqual(len(bookmark['tags']), 2)


if __name__ == '__main__':
    unittest.main()


