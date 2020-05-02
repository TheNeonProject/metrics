# A template to bootstrap TNP Backend projects

To start a new project, click on the "Use this template" button.

The `project` folder is where the main configuration will go.

It is advisable to create the rest of the apps in the project in an `app` folder with the next command:

`django-admin startproject`

And the structure of the project will remain as follows
* app/app1
* app/app2

# {PROJECT-NAME}


## Installation

### Backend

The backend run in Docker. We need to have docker (docker-engine) and docker-compose installed

```bash
docker-compose build
```

The first time we start the project locally it will be necessary to migrate the data and create a superuser

```bash
docker-compose  run  --rm backend pipenv run  python manage.py migrate
docker-compose  run  --rm backend pipenv run  python manage.py createsuperuser
```

## Execute

### Backend

```bash
docker-compose up
```

## Run tests

### Backend

```bash
docker-compose run --rm backend pipenv run coverage run --source='.' manage.py test
```
