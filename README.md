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


### Test

To run tests

```shell
docker-compse run --rm web pytest
```


### Linting

Pre-commit hooks are used to clean-up the code. Install pre-commit hooks with

```shell
pre-commit install
```

From this point each commit will run the hooks. To manually run the hooks

```shell
pre-commit run --all-files
```


## Time Slots

Time Slot are pre-determined time for appointment starting from 9am to 9pm, 30 minutes apart.
There is management command to create those

```shell
docker-compose run --rm web python manage.py create_slots
```
