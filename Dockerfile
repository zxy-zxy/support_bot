FROM python:3.7-slim

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /bot_application/requirements.txt
RUN pip install -r /bot_application/requirements.txt

COPY ./application/ /bot_application/application/
COPY ./entrypoint.sh /bot_application/entrypoint.sh

WORKDIR /bot_application/

RUN	chmod +x	/bot_application/entrypoint.sh