FROM python:3.5.2
RUN mkdir /code
ADD requirements.txt /code
RUN pip install -r /code/requirements.txt
ADD . /code
WORKDIR /code/example_app
VOLUME /code

ENTRYPOINT bash -c "python manage.py migrate --noinput && python manage.py loaddata users && python manage.py runserver 0.0.0.0:8000"
