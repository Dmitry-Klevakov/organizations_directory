#!/bin/bash

>&2 echo "Waiting for PostgreSQL"

/var/www/organizations_directory/wait-for-it.sh  -h "postgres_db" -p "5432" -t 10 -- >&2 echo "PostgreSQL is ready"
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:8000
