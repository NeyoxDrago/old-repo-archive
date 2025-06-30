import os
from gnewsclient import gnewsclient
import dialogflow_v2 as dialogflow

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "client.json"
dialogflow_session_client = dialogflow.SessionsClient()
PROJECT_ID = "worker-agent-wedmfg"

client = gnewsclient.NewsClient()


def detect_intent_from_text(text, session_id, language_code='en'):
    session = dialogflow_session_client.session_path(PROJECT_ID, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = dialogflow_session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result


def get_reply(query, chat_id):
    response = detect_intent_from_text(query, chat_id)
    print("intent",response.intent.display_name)
    if response.intent.display_name == 'topic':
        return "topic", dict(response.parameters)
    else:
        return "small_talk", response.fulfillment_text


def fetch_news(parameters):
##    return parameters
    client.language = parameters.get('language')
    client.location = parameters.get('geo-country')
    client.topic = parameters.get('topic')
    return client.get_news()[:5]


topics_keyboard = [
    ['Sports', 'Technology', 'Machine Learning'],
    ]
