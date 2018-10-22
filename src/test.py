import sqlite3
import unittest

from database import bootstrap, create_bookmark, get_bookmarks, get_bookmarks_with_tag, get_tags, get_urls, delete_bookmark

db = sqlite3.connect('./__test.db')
cursor = db.cursor()


class TestBookmarks(unittest.TestCase):
    def setUp(self):
        bootstrap(cursor)

    def test_create(self):
        seeds = [
            {
                'url': 'http://buzz.com',
                'tags': ['biz', 'bar']
            },
            {
                'url': 'https://barfoo.co',
                'tags': ['bar', 'baz']
            },
            {
                'url': 'https://foobar.com',
                'tags': ['foo', 'bar']
            }
        ]

        for seed in seeds:
            create_bookmark(seed['url'], seed['tags'], db)

        bookmarks = get_bookmarks(cursor)

        self.assertEqual(len(bookmarks), 3)
        self.assertEqual(bookmarks, seeds)

        self.assertEqual(bookmarks[0]['url'], seeds[0]['url'])
        self.assertEqual(bookmarks[1]['url'], seeds[1]['url'])
        self.assertEqual(bookmarks[2]['url'], seeds[2]['url'])

        self.assertEqual(len(bookmarks[0]['tags']), 2)
        self.assertEqual(len(bookmarks[1]['tags']), 2)
        self.assertEqual(len(bookmarks[2]['tags']), 2)

    def test_delete_bookmark(self):
        url = 'https://foobar.com'
        delete_bookmark(url, db)
        bookmarks = get_bookmarks(cursor)
        self.assertEqual(len(bookmarks), 2)

    def test_tag_query(self):
        bookmarks = get_bookmarks_with_tag(cursor, 'foo')
        self.assertEqual(len(bookmarks), 0)

        bookmarks = get_bookmarks_with_tag(cursor, 'bar')
        self.assertEqual(len(bookmarks), 2)

    def test_get_tags(self):
        tags = get_tags(cursor)
        self.assertEqual(len(tags), 4)

    def test_get_urls(self):
        urls = get_urls(cursor)
        self.assertEqual(len(urls), 2)


if __name__ == '__main__':
    unittest.main()
