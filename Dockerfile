# Use slim if possible because its 100MB compared to the 1GB standard image.
FROM docker.io/library/python:3.10-slim-bookworm

USER root
ENV PYTHONUNBUFFERED 1
RUN mkdir -p /usr/src/app \
    && groupadd -g 1000 python \
    && useradd -u 1000 -g 1000 -d /usr/src/app python \
    && chown -R python:python /usr/src

WORKDIR /usr/src/app

# First, install dependencies so that subsequent builds can leverage the layer cache if requiements.txt didn't change.
COPY requirements.txt /usr/src/app
RUN pip3 install --no-cache-dir -r requirements.txt

# Second, copy source files since they will change with each build.
COPY --chown=python . /usr/src/app/
USER python:python

# The port binding is in gunicorn.sh
EXPOSE 8000

RUN chmod +x /usr/src/app/gunicorn.sh
ENTRYPOINT /usr/src/app/gunicorn.sh
