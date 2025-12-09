FROM docker.io/library/python:3.10-slim@sha256:80619a5316afae7045a3c13371b0ee670f39bac46ea1ed35081d2bf91d6c3dbd

RUN pip install pip==25.3 setuptools==78.1.1

RUN pip install --no-cache-dir rasterio scikit-image click loguru && \
    python -c "import rasterio"

ADD app.py /app/app.py

WORKDIR /app

ENTRYPOINT []
