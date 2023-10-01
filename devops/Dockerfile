FROM python:3.9-slim as base

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y --no-install-recommends libffi-dev libpq-dev gcc musl-dev default-libmysqlclient-dev

# Install pip requirements
WORKDIR /app
#RUN chown -R nobody: /app
#USER nobody
#ENV PATH="/app/.local/bin:${PATH}"
ENV HOME=/app


COPY devops/requirements.txt .
RUN python -m pip install --upgrade pip && python -m pip install -r requirements.txt

COPY . /app

EXPOSE 4001
