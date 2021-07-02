FROM python:3.10-rc-alpine AS base

RUN adduser -D -g '' server
USER server
WORKDIR /home/server

RUN python -m venv env
ENV PATH="./env/bin:$PATH"
RUN python -m pip install --upgrade pip

FROM base AS base-env

RUN pip install flask

FROM base-env AS base-req

COPY app.py app.py

RUN export FLASK_APP=app.py
EXPOSE 5000
CMD flask run --host=127.0.0.1