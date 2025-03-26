#!/bin/bash

if [[ $APP =~ "novacture-api-pr" ]] ; then
  echo "Dump main DB"
  export PATH=$HOME/bin:$PATH
  dbclient-fetcher psql 16
  pg_dump --clean --if-exists --format c --no-owner --no-privileges --no-comments -n 'public' -n 'sequelize' --exclude-schema 'information_schema' --exclude-schema '^pg_*' --dbname $MAIN_DATABASE_URL --file dump.pgsql
  psql --dbname $DATABASE_URL
  pg_restore --clean --if-exists --no-owner --no-privileges --no-comments --dbname $DATABASE_URL dump.pgsql
fi

alembic upgrade head
