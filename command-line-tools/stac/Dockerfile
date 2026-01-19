FROM docker.io/library/python:3.12-slim
# Update base OS packages and clean up
RUN set -eux; \
    apt-get update; \
    apt-get upgrade -y; \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        gdal-bin \
        libgdal-dev \
    ; \
    rm -rf /var/lib/apt/lists/*

# Upgrade Python packaging tools
RUN pip install --no-cache-dir \
    pip>=25.3 \
    setuptools>=78.1.1

RUN pip install --no-cache-dir pystac rio_stac loguru click && \
    python -c "import rio_stac"

ADD app.py /app/app.py

WORKDIR /app

ENTRYPOINT []