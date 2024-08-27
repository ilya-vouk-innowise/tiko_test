# TIKO Test

## Installation

Prerequisites: Python 3.10+

Optionally. Install virtualenv:
```shell
pip install virtualenv
python -m virtualenv venv
source venv/bin/activate
```

Install the requirements for the development by:
```shell
pip install -r requirements.test.txt
```

In install only dependencies required for start:
```shell
pip install -r requirements.txt
```

Migrate database:
```shell
python manage.py migrate
```

Optionally. Create a superuser to access the admin panel:
```shell
python manage.py createsuperuser
```

## Run server

To start development server, please run:
```shell
python manage.py runserver localhost:8000
```

To access the application:
- Admin Panel - http://localhost:8000/admin/
- API Docs (Swagger) - http://localhost:8000/api/v1/swagger/
- API Docs (Redoc) - http://localhost:8000/api/v1/redoc/

## Development 

Run linters:
```shell
black .
flake8 .
isort .
mypy .
```

Run tests:

To run tests please set settings key `DEBUG` to true.
```shell
pytest
```