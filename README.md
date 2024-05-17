# Doc Appointment API
API for booking doctor appointment

## Running/Dev

Docker (Docker-compose) is required to run this server

### Collect Static

Run the following command to collect the static files needed to run the application

```shell
docker-compose run --rm web python manage.py collectstatic --no-input
```

Run the following to run the server

```shell
docker-compose up
```

The api docs should be available on `http://localhost:8020/api/docs`
