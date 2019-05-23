from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from google.auth.exceptions import GoogleAuthError
from google.api_core.exceptions import GoogleAPIError

from application.utils.logger_config import WrappedLogger
from application.dialogflow_api import detect_intent
from application.utils.config import Config

wrapped_logger = WrappedLogger(__file__)


class TelegramDialogBot:
    def __init__(self, token):
        self.updater = Updater(token=token)
        dp = self.updater.dispatcher
        dp.add_handler(CommandHandler('start', _start))
        dp.add_handler(MessageHandler(Filters.text, _dialog))
        dp.add_error_handler(_error)

    def start(self):
        self.updater.start_polling()
        self.updater.idle()


def _start(bot, update):
    update.message.reply_text('Hi!')


def _error(bot, update, error):
    wrapped_logger.logger.warning('Update "%s" caused error "%s"', update, error)


def _dialog(bot, update):
    language_code = 'ru'

    try:
        response = detect_intent(
            Config.DIALOGFLOW_PROJECT_ID,
            language_code,
            update.message.chat_id,
            update.message.text
        )
        update.message.reply_text(
            response.query_result.fulfillment_text
        )
    except (GoogleAuthError, GoogleAPIError) as e:
        update.message.reply_text(
            'Please, try again later.'
        )
        wrapped_logger.logger.error(
            f'An error {str(e)} has occurred during response to {update.message.chat_id}'
        )
