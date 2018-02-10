FROM python:3.6
MAINTAINER Alberto Vara "albertovara@paradigmadigital.com"
RUN mkdir /app
WORKDIR /app
ADD requirements-dev.txt requirements.txt /app/
RUN pip install -r requirements-dev.txt
ADD . /app/
ENV PYTHONUNBUFFERED=1 ENVIRONMENT=pre
CMD ["python", "manage.py", "runserver"]