### A simple, self-hosted bookmark manager

Create, store and categorise bookmarks on your own server.
Provides a web interface to categorise and store bookmarks in sqlite3.

Intentionally low-fi with minimal dependencies. 

A terminal client is in the works.

Tested on Arch Linux, Ubuntu and OSX

### Installation

With docker & docker-compose:
You will firstly need to create and `.env` file in the root of this repo.
The following are available:

```
FLASK_APP=server.py # This will likely never change unless you want to customise the entry point
FLASK_DEBUG=1 # Useful for development
DATABASE=database/example.db
PROXY_HOST=hostname
PROXY_TLS='email@example.com' or 'off'
USERNAME=bob
PASSWORD=secret
```

From there you can simply run the following:

```
docker-compose build
docker-compose up (-d)
```

Please make sure the `PROXY_HOST` is resolving correctly for TLS support.
