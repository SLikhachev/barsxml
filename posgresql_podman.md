# How to run postgres DB from podman

- First pull image from docker.io
`podman pull docker.io/msvobodin/postgres-ru:13.8`

- Second crteate local db data folder
```sh
cd ~/opt
mkdir pg13/data
```

- Third run pod as
```sh
podman run --name pg_13 \
  -v ~/opt/pg13/data:/var/lib/postgresql/data \
  -p 127.0.0.1:5432:5432 \
  -e POSTGRES_PASSWORD=password \
  -d postgres-ru:13.8
```
- 4th enter in the running pod with psql as postgres user
(this will connected to DBRM through unix socket)
`podman exec -it pg_13 psql -U postgres`

- 5th Create new database with RU locale
```sql
CREATE DATABASE hokuto LC_COLLATE='ru_RU.UTF-8' LC_CTYPE='ru_RU.UTF-8' template template0;
```

- Make copy of the DB backup to to container
`podman cp ./hokuto_1-10-25.backup pg_13:/tmp/hokuto.backup`

- 6th Restor eDatabase from backup as sql text
`podman exec -i pg_13 psql -U postgres -d hokuto < /tmp/hokuto.sql`

or as `pg_backup` output

`podman exec -it pg_13 pg_restore -U postgres -d hokuto --clean /tmp/hokuto.backup`

## How to start and stop pod

When pod running, that may be tsted as

`podman ps`

or get all containers

`podman ps -a`

in maybe stopped as

`podman stop pg_13`

Stopped container maybe started as

`podman start pg_13`

## How to remove and recreate container

To remove container you should run

`podman rm pg_13`

To recreate and run pod from image you should run

```sh
podman run --name pg_13 \
  -v ~/opt/pg13/data:/var/lib/postgresql/data \
  -p 127.0.0.1:5432:5432 \
  -e POSTGRES_PASSWORD=password \
  -d postgres-ru:13.8
```