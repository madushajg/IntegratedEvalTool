import os
from google.oauth2 import service_account
# from DB_Manager import insert_intents_into_db
from Similarity_engine import find_similar_intent

credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
credentials = service_account.Credentials.from_service_account_file(credentials_path)
PROJECT_ID = os.getenv('GCLOUD_PROJECT')

print('Credendtials from environ: {}'.format(credentials))


def detect_intent_texts(project_id, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.
    Using the same `session_id` between requests allows continuation
    of the conversation."""
    import dialogflow_v2 as dialogflow
    session_client = dialogflow.SessionsClient(credentials=credentials)

    session = session_client.session_path(project_id, session_id)
    # print('Session path: {}\n'.format(session))

    for text in texts:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)

        query_input = dialogflow.types.QueryInput(text=text_input)

        response = session_client.detect_intent(
            session=session, query_input=query_input)

        query_text = response.query_result.query_text
        intent = response.query_result.intent.display_name
        confidence = response.query_result.intent_detection_confidence
        fulfillment = response.query_result.fulfillment_text
        parameters = response.query_result.parameters

        # print('=' * 40)
        # print('Query text: {}'.format(query_text))
        # print('Detected intent: {} (confidence: {})\n'.format(intent, confidence))
        # print('Fulfillment text: {}\n'.format(fulfillment))
        # print('Parameter Entity : {}'.format(parameters))

        if fulfillment == 'unknown':
            fulfillment = find_similar_intent([str(query_text)])
            # print('Fulfillment text (by SE): {}\n'.format(fulfillment))

        # record = response.query_result
        # record = {"Query Text": query_text, "Intent": intent, "Confidence": confidence, "Fulfillment": fulfillment, "Parameters": parameters}
        # print(record)
        # insert_intents_into_db(record)
        return intent


