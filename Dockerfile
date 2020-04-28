FROM python:3

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/
RUN python -m pip install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

ADD src /usr/src/app/src
ADD elasticsearch /usr/src/app/elasticsearch
EXPOSE 8080
CMD gunicorn "src:create_app()"  --config=src/gunicorn_config.py