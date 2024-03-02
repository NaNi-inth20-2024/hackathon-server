FROM python:3.12-alpine

ARG YOUR_ENV
ENV YOUR_ENV=${YOUR_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # Poetry's configuration:
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local' \ 
  POETRY_VERSION=1.8.0

WORKDIR /src/hackathon_project
RUN apk update && \
    apk add gcc && \
    apk add libffi-dev && \
    apk add musl-dev && \
    apk add postgresql-dev && \
    apk add --no-cache bash && \
    apk --no-cache add curl && \
    apk add mariadb-dev && \
    apk add mysql-client



RUN curl -sSL https://install.python-poetry.org | python3 -
COPY pyproject.toml ./
RUN poetry install $(test "$YOUR_ENV" == production && echo "--only=main") --no-interaction --no-ansi
COPY . .

WORKDIR /src/hackathon_project/src
RUN chmod +x ../entrypoint.sh
CMD ["../entrypoint.sh"]