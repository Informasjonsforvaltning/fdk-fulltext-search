FROM python:3.8

RUN mkdir -p /app
WORKDIR /app

RUN pip install "poetry==1.6.1"
COPY poetry.lock pyproject.toml /app/

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi

ADD src /app/src
ADD elasticsearch /app/src/elasticsearch

EXPOSE 8080

CMD gunicorn --chdir src "fdk_fulltext_search:create_app()" --config=src/fdk_fulltext_search/gunicorn_config.py