FROM quay.io/fedora/python-310:310

RUN pip install --no-cache-dir pystac rio_stac loguru click && \
    python -c "import rio_stac"

ADD app.py /app/app.py

ENTRYPOINT []