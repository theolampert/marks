import unittest
from app import bootstrap, create_bookmark, get_bookmarks


class TestBookmarks(unittest.TestCase):
    def setUp(self):
        bootstrap()

    def test_create(self):
        url = 'https://foobar.com'
        tags = ['foo', 'bar']

        create_bookmark(url, tags)
        bookmarks = get_bookmarks()
        bookmark = bookmarks[0]

        self.assertEqual(len(bookmarks), 1)
        self.assertEqual(bookmark['url'], url)
        self.assertEqual(len(bookmark['tags']), 2)


if __name__ == '__main__':
    unittest.main()


