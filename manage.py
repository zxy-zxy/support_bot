import json
import sys
import argparse

from google.auth.exceptions import GoogleAuthError
from google.api_core.exceptions import GoogleAPIError

from application.utils.config import Config, ConfigurationError, validate_config
from application.utils.logger_config import WrappedLogger
from application.dialogflow_api import create_intent
from application.telegram_bot import TelegramDialogBot
from application.vk_bot import VkBot

wrapped_logger = WrappedLogger(__file__)


def create_parser():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command')

    initialize_intents_parser = subparsers.add_parser(
        'init', help=initialize_dialogflow_intents.__doc__
    )

    run_parser = subparsers.add_parser(
        'run',
    )
    run_parser.add_argument(
        'platform',
        type=str,
        help='Run bot on telegram or vk platform.'
    )

    return parser


def initialize_dialogflow_intents():
    """
    Initialize intents with provided data.
    """
    try:
        with open(Config.DIALOGFLOW_LEARNING_DATA_FILE_PATH, 'r') as file_read:
            learning_data = json.loads(file_read.read())
    except (FileNotFoundError, FileExistsError, json.JSONDecodeError) as e:
        wrapped_logger.logger.error(
            f'An error has occurred during attempt to read file: {str(e)}'
        )
        return

    for title, topic in learning_data.items():

        try:
            response = create_intent(
                Config.DIALOGFLOW_PROJECT_ID,
                title,
                'ru',
                topic['questions'],
                topic['answer']
            )
            wrapped_logger.logger.info(f'Intent has been created: {title}, {response.name}')
        except (GoogleAuthError, GoogleAPIError) as e:
            wrapped_logger.logger.error(
                f'An error has occurred during creating of intent: {title}: {str(e)}'
            )


def run_telegram_bot():
    """
    Run telegram bot.
    """
    wrapped_logger.logger.info('Attempt to start telegram bot.')
    telegram_bot = TelegramDialogBot(token=Config.TELEGRAM_BOT_TOKEN)
    telegram_bot.start()


def run_vk_bot():
    """
    Run vk bot
    """
    wrapped_logger.logger.info('Attempt to start vk bot.')
    vk_bot = VkBot()
    vk_bot.start()


def main():
    try:
        validate_config(Config)
    except ConfigurationError as e:
        sys.stdout.write(str(e))
        sys.exit(1)

    parser = create_parser()
    args = parser.parse_args()

    if args.command == 'init':
        initialize_dialogflow_intents()
    elif args.command == 'run':
        if args.platform == 'telegram':
            run_telegram_bot()
        elif args.platform == 'vk':
            run_vk_bot()
        else:
            sys.stdout.write('Unknown command. Please refer for help.')
            sys.exit(1)
    else:
        sys.stdout.write('Unknown command. Please refer for help.')
        sys.exit(1)


if __name__ == '__main__':
    main()
