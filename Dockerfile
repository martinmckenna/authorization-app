# Flask app Dockerfile
FROM python:3.9

# Install needed dependencies for our app to run.
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    musl-dev

WORKDIR /opt/app

# App non-root user
ENV GROUP=app
ENV USER=flask
ENV UID=12345
ENV GID=23456
RUN addgroup --gid "$GID" "$GROUP" \
  && adduser --uid "$UID" \
    --disabled-password \
    --gecos "" \
    --ingroup "$GROUP" \
    "$USER"

# Switch to the non-root user
USER "$USER"
ENV PATH="/home/$USER/.local/bin:${PATH}"

# Copy requirements file to our container, install, and remove
# files to we don't need to reduce the container size
COPY requirements.txt .
COPY static_requirements.txt .
RUN pip install \
    --no-cache-dir \
    --no-warn-script-location \
    --user \
    -r requirements.txt \
    -r static_requirements.txt \
  && find "/home/$USER/.local" \
    \( -type d -a -name test -o -name tests \) \
    -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
    -exec rm -rf '{}' +


# Copy app to container (with privileges to non-root user)
COPY --chown=$USER:$GROUP . .

USER "root"
RUN chmod +x scripts/app_entrypoint.sh
RUN chmod +x scripts/run_migrations.sh
USER "$USER"

# Gunicorn is run from the docker-compose file
ENTRYPOINT scripts/app_entrypoint.sh $FLASK_APP $GUNICORN_OPTIONS