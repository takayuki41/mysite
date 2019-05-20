FROM python:3.6

RUN mkdir -p /opt/services/djangoapp/src
WORKDIR /opt/services/djangoapp/src

ADD requirements.txt /opt/services/djangoapp/src/
RUN pip install -r requirements.txt

COPY . /opt/services/djangoapp/src

EXPOSE 8000

CMD ["gunicorn", "--chdir", "mysite", "--bind", ":8000", "mysite.wsgi:application"]