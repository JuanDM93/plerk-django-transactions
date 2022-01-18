# plerk-django-transactions

Django demo project

## Description

This is an api demo built on django's [rest](https://www.django-rest-framework.org/) framework.

### Service Endpoints

```endpoints
/admin

/api/summary
/api/companies/{company_id}
```

## Run options

### Local python virtual environment

#### Database

This django project uses a postgres database by default, so you need to create a database first and modify .env, as well as [settings.py](https://docs.djangoproject.com/en/4.0/ref/databases/), as needed.

#### Setup

Once cloned, create new [python environment](https://docs.python.org/3/tutorial/venv.html) "venv", then activate it

```bash
python -m venv venv
source venv/bin/activate
```

Install requirements

```bash
python -m pip install -U pip setuptools
pip install -r requirements.txt
```

Now, create an [.env](https://django-environ.readthedocs.io/en/latest/) file, as in .env.example file, and run `python manage.py makemigrations` and `python manage.py migrate`

Run server (where manage.py is)

```bash
python manage.py runserver <PORT>
```

## License

[MIT License](https://choosealicense.com/licenses/mit/)
