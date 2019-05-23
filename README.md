# Python support-bot equipped with dialogflow.

This application is designed to make life of your support team easier. 
Main idea is that bot keeps the conversation going, because it's backend operated with [dialogflow](https://dialogflow.com/).

* [Vk](https://vk.com)
* [Telegram](https://telegram.org/)

![](data/screen.gif)

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
Application using telegram bot for logging as well.
* Obtain a token for your logging bot from [botfather](https://core.telegram.org/bots). This is required for 
TELEGRAM_LOGGER_BOT_TOKEN environment variable.
* Provide TELEGRAM_LOGGER_CHAT_ID at your .env file. This is the chat id where bot is going to send you it's messages.

#### Before you go
* Then, configure your environments variables. Example.env file is provided.
* Before run your bot please initialize intents at dialogflow.

To initialize [dialogflow](https://dialogflow.com/) intents please run:
```bash
python manage.py init
```

#### To run on your local computer
Build your services with docker-compose:
```bash
docker-compose -f docker-compose-dev.yml build
```
If you want to run telegram bot, run:
```bash
docker-compose -f docker-compose-dev.yml run support-bot-telegram
```
And for Vk bot:
```bash
docker-compose -f docker-compose-dev.yml run support-bot-vk
```

#### Deploy with Heroku
Each type of bot has it's own branch. 
While deploying application on Heroku with GitHub deployment method select the branch you are interested in.

Then, login with [Heroku cli](https://devcenter.heroku.com/articles/heroku-cli):
```bash
heroku login
```
Setup:
```bash
heroku ps:scale bot=1 --app <your_application_name_here>
heroku logs --tail --app <your_application_name_here>
```