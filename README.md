# Python support-bot equipped with dialogflow.

This is a chatbot application which is designed to make life of your support team easier. 
Main idea is that bot keeps the conversation going, since it's backend operated with [dialogflow](https://dialogflow.com/).

Currently 2 platforms are supported:

* [Vk](https://vk.com)
* [Telegram](https://telegram.org/)

![](data/bot_example.gif)

### Usage

Before you can run application you must do some preliminary actions:

* Create new project at [dialogflow](https://dialogflow.com/).
* Create new service account and grant access to your dialogflow project at [Google cloud console](https://console.cloud.google.com) project 
page.

#### Telegram configuration
* Obtain a token for your bot from [botfather](https://core.telegram.org/bots).

#### Vk configuration
* Create a group at [https://vk.com](Vk).
* Obtain a group token.

#### Logger configuration
Application uses telegram bot for logging as well.
* Obtain a token for your logging bot from [botfather](https://core.telegram.org/bots). This is required for 
TELEGRAM_LOGGER_BOT_TOKEN environment variable.
* Fill TELEGRAM_LOGGER_CHAT_ID env. variable with chat id which is intended for receiving log messages.

#### Google services configuration
* Put your google service account credentials into application folder at data/google_credentials.json
or provide full filepath at entrypoint.sh.
* Before you can run your bot you need to initialize intents at dialogflow.

#### Running on local environment
Build with docker-compose:
```bash
docker-compose -f docker-compose-dev.yml build
```

Initialize [dialogflow](https://dialogflow.com/) intents:
```bash
docker-compose -f docker-compose-dev.yml run init-intents
```

To run telegram-bot:
```bash
docker-compose -f docker-compose-dev.yml run support-bot-telegram
```
To run vk-bot:
```bash
docker-compose -f docker-compose-dev.yml run support-bot-vk
```

#### Deploy with Heroku
While deploying application on Heroku with GitHub deployment method select the branch which you are interested in.

Login with [Heroku cli](https://devcenter.heroku.com/articles/heroku-cli):
```bash
heroku login
```
Setup google service account credentials with:
```bash
heroku config:set GOOGLE_APPLICATION_CREDENTIALS="$(< credentials.json)"
```
Run application and track logs:
```bash
heroku ps:scale bot-telegram=1 --app <your_application_name_here>
heroku ps:scale bot-vk=1 --app <your_application_name_here>
heroku logs --tail --app <your_application_name_here>
```