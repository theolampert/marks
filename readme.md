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


#### Management

Right now you can export json using the following:
```sh
./scripts/manage.sh export-json > src/export.json
```

And import it like so:
```sh
./scripts/manage.sh import-json ./export.json
```

You can also download bookmark json from your remote instance using curl:
```sh
export TOKEN=$(curl -XPOST http://<your-instance>/login -d 'username=bob' -d 'password=secret')
curl http://<your-instance>/bookmarks?token=$TOKEN > export.json
```

#### Roadmap

- [ ] Ability to edit urls and tags
- [ ] Browser extension clients
- [ ] CLI client
- [ ] Backup scripts and automated backups
- [ ] Better import / export tools including more formats
