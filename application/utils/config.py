import os


class ConfigurationError(Exception):
    pass


class Config:
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    DIALOGFLOW_PROJECT_ID = os.getenv('DIALOGFLOW_PROJECT_ID')
    DIALOGFLOW_LEARNING_DATA_FILE_PATH = os.getenv('DIALOGFLOW_LEARNING_DATA_FILE_PATH')

    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    TELEGRAM_LOGGER_BOT_TOKEN = os.getenv('TELEGRAM_LOGGER_BOT_TOKEN')
    TELEGRAM_LOGGER_CHAT_ID = os.getenv('TELEGRAM_LOGGER_CHAT_ID')

    VK_GROUP_TOKEN = os.getenv('VK_GROUP_TOKEN')

    required = [
        'GOOGLE_APPLICATION_CREDENTIALS',
        'DIALOGFLOW_PROJECT_ID',
        'DIALOGFLOW_LEARNING_DATA_FILE_PATH',
        'TELEGRAM_BOT_TOKEN',
        'TELEGRAM_LOGGER_BOT_TOKEN',
        'TELEGRAM_LOGGER_CHAT_ID',
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
