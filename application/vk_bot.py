import random

from google.auth.exceptions import GoogleAuthError
from google.api_core.exceptions import GoogleAPIError
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from application.dialogflow_api import detect_intent
from application.utils.logger_config import WrappedLogger
from application.utils.config import Config

wrapped_logger = WrappedLogger(__file__)


class VkBot:
    default_fallback_intent = 'default fallback intent'

    def __init__(self):
        self._vk_session = vk_api.VkApi(token=Config.VK_GROUP_TOKEN)
        self._longpoll = VkLongPoll(self._vk_session)

    def start(self):
        _vk_api = self._vk_session.get_api()
        for event in self._longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                self._dialog(event, _vk_api)

    def _dialog(self, event, _vk_api):
        language_code = 'ru'

        try:
            response = detect_intent(
                Config.DIALOGFLOW_PROJECT_ID,
                language_code,
                event.user_id,
                event.text
            )

            response_intent = response.query_result.intent.display_name
            response_intent = response_intent.strip().lower()

            if response_intent == VkBot.default_fallback_intent:
                pass
            else:
                wrapped_logger.logger.warning(
                    f'Could not detect proper intent, please reply in manual mode.'
                )
                _vk_api.messages.send(
                    user_id=event.user_id,
                    message=response.query_result.fulfillment_text,
                    random_id=random.randint(1, 1000)
                )

        except (GoogleAuthError, GoogleAPIError) as e:
            _vk_api.messages.send(
                user_id=event.user_id,
                message='Please, try again later.',
                random_id=random.randint(1, 1000)
            )
            wrapped_logger.logger.error(
                f'An error {str(e)} has occurred during response to {event.user_id}'
            )
