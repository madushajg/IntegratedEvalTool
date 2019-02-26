from pprint import pprint
import os
import requests

TOKEN = os.getenv('API_TOKEN')
CTYPE = os.getenv('API_CONTENT_TYPE')

header = {'Authorization': TOKEN, 'content-type': CTYPE}


def enter_new_entity(entities, url_ds, entity_name):
    head = """{
  "entries": ["""

    tail = "\n  ],\"name\": \"" + entity_name + "\" }"

    val = "{\n      \"value\": \"9999\" \n    , \n      \"synonyms\": ['4444'] \n    }"
    val_head = ", \n    {\n      \"value\": \""
    val_tail = "\" "
    entry_tail = "\n    }"

    syn_head = ", \n     \"synonyms\": ["
    syn_tail = "] \n"
    print(entities)
    for a in entities:
        entry = val_head + a[0] + val_tail + syn_head + "\"" + a[1] + "\"" + ", \"" + a[
            2] + "\"" + syn_tail + entry_tail
        val = val + entry

    payload = head + val + tail
    print(payload)
    req = requests.put(url_ds, data=payload, headers=header)
    pprint(req.json())
    print("Entities successfully added")


# def enter_filename_entity(entities, url):
#     head = """{
#   "entries": ["""
#
#     tail = """\n  ],
#   "name": "Dataset_Name"
# }"""
#
#     val = "{\n      \"value\": \"999\" \n    },{\n      \"value\": \"444\" \n    }"
#     val_head = ", \n    {\n      \"value\": \""
#     val_tail = "\" \n    }"
#     for a in entities:
#         entry = val_head + a + val_tail
#         val = val + entry
#
#     payload = head + val + tail
#     print(payload)
#     r = requests.put(url, data=payload, headers=header)
#     pprint(r.json())
#     print("Entities successfully added")


def delete_entries(entities, url):
    body = """[\"9999\""""
    for a in entities:
        body = body + ",\"" + a + "\""

    payload = body + "]"

    print(payload)
    d = requests.delete(url + '/entries', data=payload, headers=header)
    print(d.json())


if __name__ == '__main__':
    attributes = ['restaurant_id', 'restaurant_name', 'country_code', 'city', 'longitude', 'latitude',
                  'average_cost_for_two', 'currency', 'has_table_booking', 'has_online_delivery', 'is_delivering_now',
                  'switch_to_order_menu', 'price_range', 'aggregate_rating', 'rating_color', 'rating_text', 'votes',
                  'cuisines']

    attributes_mul = [['restaurant_id', 'Restaurant ID', 'column1'], ['restaurant_name', 'Restaurant Name', 'column2'],
                      ['country_code', 'Country Code', 'column3'], ['city', 'City', 'column4'],
                      ['longitude', 'Longitude', 'column5'],
                      ['latitude', 'Latitude', 'column6'], ['average_cost_for_two', 'Average Cost for two', 'column7'],
                      ['currency', 'Currency', 'column8'], ['has_table_booking', 'Has Table booking', 'column9'],
                      ['has_online_delivery', 'Has Online delivery', 'column10'],
                      ['is_delivering_now', 'Is delivering now', 'column11'],
                      ['switch_to_order_menu', 'Switch to order menu', 'column12'],
                      ['price_range', 'Price range', 'column13'],
                      ['aggregate_rating', 'Aggregate rating', 'column14'],
                      ['rating_color', 'Rating color', 'column15'],
                      ['rating_text', 'Rating text', 'column16'], ['votes', 'Votes', 'column17'],
                      ['cuisines', 'Cuisines', 'column18']]

    attributes_ds = [['filtered_zomato.csv', 'Filtered Zomato.csv', 'dataset']]

    url_ds_attributes = 'https://api.dialogflow.com/v1/entities/ds_attributes'
    url_ds_name = 'https://api.dialogflow.com/v1/entities/Dataset_Name'
    enter_new_entity(attributes_ds, url_ds_name, 'Dataset_Name')

    # enter_new_entity(attributes_mul, url_ds_attributes, 'ds_attributes')
    # delete_entries(attributes, url_ds_attributes)
