import json

import dialogflow_v2 as dialogflow
from google.oauth2 import service_account

from application.utils.config import Config


def load_credentials_from_config():
    service_account_info = json.loads(Config.GOOGLE_APPLICATION_CREDENTIALS)
    credentials = service_account.Credentials.from_service_account_info(
        service_account_info)
    return credentials


def create_intent(
        project_id, display_name, language_code, training_phrases_parts, messages_texts
):

    credentials = load_credentials_from_config()

    intents_client = dialogflow.IntentsClient(credentials=credentials)
    parent = intents_client.project_agent_path(project_id)

    training_phrases = []

    for training_phrases_part in training_phrases_parts:
        part = dialogflow.types.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.types.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    if isinstance(messages_texts, (str, bytes, bytearray)):
        messages_texts = [messages_texts]

    text = dialogflow.types.Intent.Message.Text(text=messages_texts)
    message = dialogflow.types.Intent.Message(text=text)

    intent = dialogflow.types.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(parent, intent, language_code=language_code)
    return response


def detect_intent(project_id, language_code, session_id, text):
    credentials = load_credentials_from_config()

    session_client = dialogflow.SessionsClient(credentials=credentials)
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(session=session, query_input=query_input)
    return response
