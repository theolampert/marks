### A bookmarking manager from the dark ages

Create, store and categorise bookmarks on your own server.
Provides a web interface to categorise and store bookmarks in sqlite3.

Intentionally low-fi with minimal dependencies. 
You'll will need a recent version of python or optionally docker.

The web ui is incredibly basic and will run on a potato. 
A terminal client is in the works.

Tested on Arch Linux and OSX

### Installation

With plain python:
```
pip install -r requirements.txt
export FLASK_APP=server.py
flask run
# or
python -m flask run
```

With docker & docker-compose:
```
docker-compose build
docker-compose up (-d)
```
