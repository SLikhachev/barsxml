# How to run postgres DB from podman

podman pull postgres:13

cd ~/opt
mkdir /pg13/data/

podman run --name pg_13 \
  -v /home/aughung/opt/pg13/data:/var/lib/postgresql/data \
  -e POSTGRES_PASSWORD=boruh \
  -d postgres-ru:13.8

podman exec -it pg_13 bash

CREATE DATABASE hokuto LC_COLLATE='ru_RU.UTF-8' LC_CTYPE='ru_RU.UTF-8' template template0;

podman cp ./hokuto_1-10-25.backup pg_13:/tmp/hokuto.backup

podman exec -i pg_13 psql -U postgres -d hokuto < /tmp/hokuto.sql
podman exec -it pg_13 pg_restore -U postgres -d hokuto --clean /tmp/hokuto.backup

