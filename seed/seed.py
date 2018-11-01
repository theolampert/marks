import json
from random import randint
from faker import Faker
fake = Faker()

tag_list = ['cs', 'programming', 'color', 'learning', 'design', 'architecture',
        'bookmarks', 'own-project', 'open-source', 'read-later', 'queue',
        'a2-german', 'german', 'german-lessons']

bookmarks = []

for _ in range(300):
    bookmark = {}
    bookmark['url'] = fake.url()
    bookmark['tags'] = fake.words(nb=randint(1, 10), ext_word_list=tag_list, unique=True)
    bookmarks.append(bookmark)

print(json.dumps(bookmarks))
