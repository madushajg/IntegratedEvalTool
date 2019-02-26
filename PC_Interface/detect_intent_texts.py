import os
from google.oauth2 import service_account
from pseudo_manager import generate_pseudo_code
from Similarity_engine import find_similar_intent
from entities import entity_extractor
import json

credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
credentials = service_account.Credentials.from_service_account_file(credentials_path)
PROJECT_ID = os.getenv('GCLOUD_PROJECT')
SESSION_ID = 'session_pc'

print('Credendtials from environ: {}'.format(credentials))
# /media/arshad/Data/FYP/FYP/UserSpecs2PseudoCode/PC_Interface
# /media/madusha/DA0838CA0838A781/PC_Interface/Resources/identification

class PseudoGen:
    extract = entity_extractor.Extractor()
    identification = open('/media/arshad/Data/FYP/FYP/UserSpecs2PseudoCode/PC_Interface/Resources/identification').read()
    idnt_map = {}
    wildcard = {"TARGET_CLASS": '', 'DATASET': '',  'ALGORITHM': 'SVM'}
    st_array, st_values, varn, var_value, rn_array, element, rn_num = ([] for i in range(7))

    for k, line in enumerate(identification.split("\n")):
        try:
            if line is not '':
                content = line.split(',')
            idnt_map[content[0]] = (content[1])
        except:
            print("Unable to locate identification map")


def line_manipulator(pc_lines, ds_name):
    pg = PseudoGen()
    pg.wildcard['DATASET'] = ds_name
    full_pc = ''
    spc_lines = []
    for l in pc_lines:
        pc = detect_intent_texts(PROJECT_ID, SESSION_ID, l, 'en-US', pg)
        full_pc = full_pc + '\n' + str(pc)
        spc_lines.append(pc)

    json_dump = json.dumps(pg.wildcard)
    f = open("wildcard.json", "w")
    f.write(json_dump)
    f.close()

    return [full_pc, spc_lines]


def detect_intent_texts(project_id, session_id, text, language_code, pseudo_gen):
    """Returns the result of detect intent with texts as inputs.
    Using the same `session_id` between requests allows continuation
    of the conversation."""
    import dialogflow_v2 as dialogflow
    session_client = dialogflow.SessionsClient(credentials=credentials)

    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.types.TextInput(
        text=text, language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session, query_input=query_input)

    query_text = response.query_result.query_text
    fulfillment = response.query_result.fulfillment_text

    print('=' * 40)

    if fulfillment == 'unknown':
        print("Default fallback")
        fulfillment = find_similar_intent(str(query_text))
        response.query_result.intent.display_name = fulfillment[0]
        print('Fulfillment text (by SE): {} (similarity: {})\n'.format(fulfillment[0], fulfillment[1]))

    pseudo_code = generate_pseudo_code(response, pseudo_gen)
    return pseudo_code


if __name__ == '__main__':
    lines = ['initialize integer variable named F with value 90',
             'add \'They are competetive\' to variable mal', 'assign 89.6 to variable rt',
             'find accuracy of model']
    # full_corpus = open('/media/madusha/DA0838CA0838A781/PC_Interface/entities/testing')
    # lines = [line for line in full_corpus.readlines() if line.strip()]
    pg = PseudoGen()
    # for line in lines:
    #     detect_intent_texts(PROJECT_ID, 'df', line, 'en-US', pg)

    line_manipulator(lines, 'filtered_zomato.csv')
