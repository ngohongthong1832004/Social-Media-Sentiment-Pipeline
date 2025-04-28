FROM apache/superset:latest

USER root

RUN pip install --no-cache-dir sqlalchemy-trino \
    && pip install --no-cache-dir Pillow

USER superset
