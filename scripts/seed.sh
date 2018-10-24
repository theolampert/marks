rm database/database.db
python3 seed/seed.py > src/export.json
sh scripts/manage.sh import-json ./export.json