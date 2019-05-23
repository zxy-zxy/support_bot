"""
Purpose of WrappedLogger class is to avoid
initialization errors of TelegramHandler instance.
If we would try to access directly to logger from
get_logger() function at the runtime it won't give us properly initialized
logger.
In order to keep logger variable global for each module, we have to initialize
logger at first interaction.
"""


import sys
import logging

import telegram

from application.utils.config import Config

FORMATTER = logging.Formatter(
    '%(asctime)s — %(name)s — %(levelname)s — %(message)s'
)


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


def _get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def _get_telegram_handler():
    telegram_handler = TelegramHandler(
        Config.TELEGRAM_LOGGER_BOT_TOKEN,
        Config.TELEGRAM_CHAT_ID
    )
    telegram_handler.setFormatter(FORMATTER)
    return telegram_handler


def _get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    logger.addHandler(_get_console_handler())
    logger.addHandler(_get_telegram_handler())
    logger.propagate = False
    return logger


class WrappedLogger:
    def __init__(self, name):
        self.logger_name = name
        self._logger = None

    @property
    def logger(self) -> logging.Logger:
        if self._logger is None:
            self._logger = _get_logger(self.logger_name)
        return self._logger
