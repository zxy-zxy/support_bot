import os
import sys
import logging.config

import telegram

sys.path.append(
    os.path.abspath(os.path.dirname(__file__))
)


class ConfigurationError(Exception):
    pass


class Config:
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    DIALOGFLOW_PROJECT_ID = os.getenv('DIALOGFLOW_PROJECT_ID')
    DIALOGFLOW_LEARNING_DATA_FILE_PATH = os.getenv('DIALOGFLOW_LEARNING_DATA_FILE_PATH')

    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    VK_GROUP_TOKEN = os.getenv('VK_GROUP_TOKEN')

    required = [
        'GOOGLE_APPLICATION_CREDENTIALS',
        'DIALOGFLOW_PROJECT_ID',
        'DIALOGFLOW_LEARNING_DATA_FILE_PATH',
        'TELEGRAM_BOT_TOKEN',
        'VK_GROUP_TOKEN',
    ]


def validate_config(config):
    errors = []
    for key in config.required:
        if not getattr(Config, key):
            errors.append(f'Environment variable {key} has not been configured properly.')
    if errors:
        error_message = '\n'.join(errors)
        raise ConfigurationError(error_message)


class TelegramHandler(logging.Handler):
    def __init__(self, telegram_token, telegram_chat_id):
        super().__init__()
        self._bot = telegram.Bot(
            token=telegram_token)
        self._telegram_chat_id = telegram_chat_id

    def emit(self, record):
        formatted_record = self.format(record)
        self._bot.send_message(
            chat_id=self._telegram_chat_id,
            text=formatted_record
        )


logconfig = {
    'version': 1,
    'formatters': {
        'standard': {
            'format': '%(asctime)s — %(name)s — %(levelname)s — %(message)s'
        }
    },
    'handlers': {
        'default': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'level': 'INFO',
        },
        'telegram': {
            'class': 'settings.TelegramHandler',
            'level': 'INFO',
            'telegram_token': os.getenv('TELEGRAM_LOGGER_BOT_TOKEN'),
            'telegram_chat_id': os.getenv('TELEGRAM_LOGGER_CHAT_ID')
        }
    },
    'loggers': {
        '': {
            'handlers': ['default', 'telegram'],
            'level': 'INFO',
            'propagate': True
        }
    }
}
logging.config.dictConfig(logconfig)

FORMATTER = logging.Formatter(
    '%(asctime)s — %(name)s — %(levelname)s — %(message)s'
)
