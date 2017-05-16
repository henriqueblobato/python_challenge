FROM tiangolo/uwsgi-nginx-flask:flask

COPY ./app /app
RUN apt-get update
RUN apt-get install -y python-dev libmysqlclient-dev
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
COPY . /tmp/
RUN mkdir -p /home/upload
