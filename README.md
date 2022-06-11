# Just forked for code storate and study

Please use the org. space https://github.com/mdn/django-locallibrary-tutorial if you don't know what I am doing.

To start up this django server. You should request docker install.

## build image

```shell
git clone https://github.com/WindoC/django-locallibrary-tutorial
cd django-locallibrary-tutorial
docker build -t django-example .
```

## Start the playground

Notice: Make sure you are in the folder django-locallibrary-tutorial

Start the container at the backgroup.

```shell
docker run -d -p 8000:8000 -v $(pwd):/usr/src/app --name django-playground django-example
```

remark: `-v $(pwd):/usr/src/app` make you can modify the code outside from the container

Some django init command may need for first run.

```shell
docker exec -it django-playground python manage.py makemigrations
docker exec -it django-playground python manage.py migrate
docker exec -it django-playground python manage.py createsuperuser # Create a superuser
```

Other command you may what to use. Just add the docker prefix before you command `docker exec -it django-playground <your command>`

Example: 

```shell
docker exec -it django-playground python manage.py collectstatic
docker exec -it django-playground python manage.py test # Run the standard tests. These should all pass.
```

Also, you can get into the shell CMD by:

```shell
docker exec -it django-playground bash
```

### How to play the playground

Check running log:

```shell
docker logs django-playground
```

if too many old log. Add `--since 3m` to get the last 3 mintues log. Or add `--tail 100` to get last 100 line

```shell
docker logs --since 3m django-playground
docker logs --tail 100 django-playground
```

if you what to monitor the log continuously. Add `-f`

```shell
docker logs -f django-playground
```

To stop it by:

```shell
docker stop django-playground
```

And you can start it again by:

```shell
docker start django-playground
```

Or if you need to restart it:

```shell
docker restart django-playground
```

To remove and clear your playground

```shell
docker stop django-playground
docker rm django-playground
```

# Django Local Library

Tutorial "Local Library" website written in Django.

For detailed information about this project see the associated [MDN tutorial home page](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Tutorial_local_library_website).

## Overview

This web application creates an online catalog for a small local library, where users can browse available books and manage their accounts.

The main features that have currently been implemented are:

* There are models for books, book copies, genre, language and authors.
* Users can view list and detail information for books and authors.
* Admin users can create and manage models. The admin has been optimised (the basic registration is present in admin.py, but commented out).
* Librarians can renew reserved books

![Local Library Model](https://raw.githubusercontent.com/mdn/django-locallibrary-tutorial/master/catalog/static/images/local_library_model_uml.png)


## Quick Start

To get this project up and running locally on your computer:
1. Set up the [Python development environment](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/development_environment).
   We recommend using a Python virtual environment.
   > **Note:** This has been tested against Django 3.1.2 (and may not work or be "optimal" for other versions).
1. Assuming you have Python setup, run the following commands (if you're on Windows you may use `py` or `py -3` instead of `python` to start Python):
   ```
   pip3 install -r requirements.txt
   python3 manage.py makemigrations
   python3 manage.py migrate
   python3 manage.py collectstatic
   python3 manage.py test # Run the standard tests. These should all pass.
   python3 manage.py createsuperuser # Create a superuser
   python3 manage.py runserver
   ```
1. Open a browser to `http://127.0.0.1:8000/admin/` to open the admin site
1. Create a few test objects of each type.
1. Open tab to `http://127.0.0.1:8000` to see the main site, with your new objects.
