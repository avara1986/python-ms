FROM python:3.6
EXPOSE 5000
MAINTAINER Alberto Vara "albertovara@paradigmadigital.com"
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app/
RUN pip install -r requirements.txt
ADD . /app/
ENV PYTHONUNBUFFERED=1 ENVIRONMENT=pre
CMD ["python", "manage.py", "runserver", "-h", "0.0.0.0"]