FROM quay.io/fedora/python-310:310

RUN pip install --no-cache-dir rasterio click loguru && \
    python -c "import rasterio"

ADD app.py /app/app.py

WORKDIR /app

ENTRYPOINT []

