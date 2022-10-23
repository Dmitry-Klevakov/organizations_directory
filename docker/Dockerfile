FROM python:3.10-bullseye

ENV POETRY_VERSION=1.2.2 \
    POSTGRES_DB=organizations_directory \
    POSTGRES_HOST=postgres_db \
    POSTGRES_PORT=5432 \
    POSTGRES_USER=postgres \
    POSTGRES_PASSWORD=pass \
    DJANGO_SETTINGS_MODULE=conf.settings \
    PYTHONUNBUFFERED=1

RUN mkdir -p var/www/organizations_directory
COPY . var/www/organizations_directory/
WORKDIR var/www/organizations_directory
RUN pip3 install --upgrade pip && \
    pip install "poetry==$POETRY_VERSION" && \
    poetry config virtualenvs.create false && \
    poetry install && \
    apt-get update && apt-get install -y curl && \
    curl -O https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh && \
    chmod +x wait-for-it.sh && \
    chmod +x docker/docker-entrypoint.sh
ENTRYPOINT ["docker/docker-entrypoint.sh"]
