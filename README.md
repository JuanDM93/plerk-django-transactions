# plerk-django-transactions

Django demo project

## Description

This is an api demo built on django's [rest](https://www.django-rest-framework.org/) framework.

It consists on a simple api that evaluates transactions from a db and generates reports.

### Database

This django project uses a postgres database by default. Create a database first and modify .env as needed, as well as [settings.py](https://docs.djangoproject.com/en/4.0/ref/databases/).

This project is built based on a `test_database.csv` file, which contains the transactions to be imported as follows:

```bash
python manage.py import_csv docs/test_database.csv
```

### Service Endpoints

The api has the following endpoints:

```endpoints
/admin

/api/summaries
/api/summaries/{company_id}

CRUD
/api/companies
/api/companies/{company_id}

/api/transactions
/api/transactions/{transaction_id}

/docs
/.../swagger
/.../redoc
```

However, in order to access the api endpoints, you need to use basic authentication. You can create a superuser with the following command:

```bash
python manage.py createsuperuser
```

## Run options

It is already deployed on heroku, however, it is not accessible withouth valid credentials.

URL = `https://pydj-m1ch-plerk.herokuapp.com`

### Local python virtual environment

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

### Heroku

This service is available on [Heroku](https://www.heroku.com/), so you can deploy it there.

To deploy, run `heroku create`

Veify that the environment variables are set correctly

Then, run `git push heroku master`

## License

[MIT License](https://choosealicense.com/licenses/mit/)
