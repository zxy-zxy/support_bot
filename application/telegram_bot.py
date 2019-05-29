import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from google.auth.exceptions import GoogleAuthError
from google.api_core.exceptions import GoogleAPIError

from dialogflow_api import detect_intent
from settings import Config


class TelegramDialogBot:
    def __init__(self, token):
        self.updater = Updater(token=token)
        dp = self.updater.dispatcher
        dp.add_handler(CommandHandler('start', self._start))
        dp.add_handler(MessageHandler(Filters.text, self._dialog))
        dp.add_error_handler(self._error)
        self._logger = logging.getLogger(__file__)

    def start(self):
        self.updater.start_polling()
        self.updater.idle()

    def _start(self, bot, update):
        self._logger.info('hello')
        update.message.reply_text('Hi!')

    def _error(self, bot, update, error):
        self._logger.warning('Update "%s" caused error "%s"', update, error)

    def _dialog(self, bot, update):
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
            self._logger.error(
                f'An error {str(e)} has occurred during response to {update.message.chat_id}'
            )
