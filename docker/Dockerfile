FROM python:3.10-bullseye

RUN mkdir -p var/www/organizations_directory
COPY . var/www/organizations_directory/
ENV POETRY_VERSION=1.2.2 \
    POSTGRES_DB=organizations_directory \
    POSTGRES_HOST=postgres_db \
    POSTGRES_PORT=5432 \
    POSTGRES_USER=postgres \
    POSTGRES_PASSWORD=pass \
    DJANGO_SETTINGS_MODULE=conf.settings \
    PYTHONUNBUFFERED=1

RUN cd var/www/organizations_directory && pip3 install --upgrade pip && pip install "poetry==$POETRY_VERSION" && poetry config virtualenvs.create false && poetry install

WORKDIR var/www/organizations_directory
RUN apt-get update && apt-get install -y curl
RUN curl -O https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh
RUN chmod +x wait-for-it.sh
RUN chmod +x docker/docker-entrypoint.sh
ENTRYPOINT ["docker/docker-entrypoint.sh"]
