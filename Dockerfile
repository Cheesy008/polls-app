FROM python:3.9.5-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/* /var/lib/cache/* /var/log/*

# Requirements are installed here to ensure they will be cached.
COPY requirements.txt /

RUN pip install --no-cache-dir -r /requirements.txt && rm /requirements.txt

COPY . /code

WORKDIR /code

CMD ["/bin/sh", "entrypoint.sh"]
