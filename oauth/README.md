### Basics

1. Activate a virtualenv
1. Install the requirements

### Set Environment Variables

Update *project/config.py*, and then run:

```sh
XXXX
```

or

```sh
XXX
```

Set a SECRET_KEY:

```sh
$ export SECRET_KEY="change_me"
```

### Create DB

Create the databases in `psql`:

```sh
$ psql
# create database mydatabase
# create database mydatabase_tests
# \q
```

Create the tables and run the migrations:

```sh
$ python manage.py create_db
```

### Run the Application

```sh
$ python manage.py runserver
```

Access the application at the address [http://localhost:5000/](http://localhost:5000/)

> Want to specify a different port?

> ```sh
> $ python manage.py runserver -h 0.0.0.0 -p 8080
> ```

### Testing

Without coverage:

```sh
$ python manage.py test
```

With coverage:

```sh
$ python manage.py cov
```
