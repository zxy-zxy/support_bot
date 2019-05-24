FROM python:3.7-slim

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /bot_application/requirements.txt
RUN pip install -r /bot_application/requirements.txt


COPY .env /bot_application/.env
COPY ./data/ /bot_application/data/
COPY ./application/ /bot_application/application/
COPY ./entrypoint-telegram.sh /bot_application/entrypoint-telegram.sh
COPY ./entrypoint-vk.sh /bot_application/entrypoint-vk.sh
COPY manage.py /bot_application/manage.py

WORKDIR /bot_application/

RUN	chmod +x	/bot_application/data/google_credentials.json
RUN	chmod +x	/bot_application/entrypoint-telegram.sh
RUN	chmod +x	/bot_application/entrypoint-vk.sh