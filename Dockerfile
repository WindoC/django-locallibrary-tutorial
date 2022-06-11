FROM python:3.9

RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
		sqlite3 \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY ./ /usr/src/app

RUN cd /usr/src/app \
 && pip install -r /usr/src/app/requirements.txt \
 && python manage.py makemigrations \
 && python manage.py migrate

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
