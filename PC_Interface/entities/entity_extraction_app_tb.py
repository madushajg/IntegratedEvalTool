import re
from pprint import pprint
import os
import time
from google.oauth2 import service_account
import test_detect_intent
from entities import create_attribute_dict, entity_extractor

credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
credentials = service_account.Credentials.from_service_account_file(credentials_path)
PROJECT_ID = os.getenv('GCLOUD_PROJECT')

# full_corpus = open('/media/madusha/DA0838CA0838A781/PC_Interface/entities/processed_lines.txt')
full_corpus = open('/media/madusha/DA0838CA0838A781/PC_Interface/entities/testing')
lines = [line for line in full_corpus.readlines() if line.strip()]

regex_var = r"\b((([Vv]ariable)|([Nn]ame)|([Ll]ist)|([Aa]rray)|([Ii]mport)|([Uu]se)|([Ii]nstance)|([Mm]odel))\b)|="
regex_num = r"\d+\.?\d*\b"
regex_import = r"\b(([Ii]mport)|([Uu]se)|([Ii]nbuilt)|([Ss]uitable)|([Aa]ppropriate))\b"
regex_features = r"\b(([Cc]olumns)|([Dd]rop)|([Cc]olumn)|([Ff]eatures)|([Ff]eature)|([Aa]ttribute)|([" \
                 r"Nn]ormalization)|([Nn]umerize)|([Uu]se)|([Nn]umerization))\b "
regex_svalues = r"\b(([Ii]mport)|([Ll]ibrary)|([Dd]isplay)|([Pp]rint)|([Pp]rintln))\b"


def generate_entities(extractor, req_ent, defined_entities):
    start = time.time()
    print(start)
    for line in lines:
        print(line)
        intention = test_detect_intent.detect_intent_texts(PROJECT_ID, 'fake', [line], language_code='en')
        print(intention)
        req_ent_int = req_ent[intention]
        print(req_ent_int)
        if 'value' in req_ent_int and 'var_name' in req_ent_int:
            entities = list(extractor.extract_entities(line))
            pprint(entities)
            params = entities_varname_value(entities, req_ent_int)
            try:
                print('var name : {}'.format(params[0]))
                print('value : {}'.format(params[1]))
            except:
                print('var_name and value not received')
            print('*' * 40)

        elif 'N' in req_ent_int:
            print('No need of entity')
            print('*' * 40)

        elif 'var_name' in req_ent_int and len(req_ent_int) == 1:
            entities = list(extractor.extract_entities(line))
            pprint(entities)
            param = entities_varname(entities)
            try:
                print('var name : {}'.format(param))
            except:
                print('var_name is not received')
            print('*' * 40)

        elif 'def_value' in req_ent_int and len(req_ent_int) == 1:
            entities = list(extractor.extract_entities(line))
            pprint(entities)
            param = entities_def_value(entities, defined_entities)
            try:
                print('var name : {}'.format(param))
            except:
                print('var_name is not received')
            print('*' * 40)

        elif 'mul_values' in req_ent_int and len(req_ent_int) == 1:
            attributes = create_attribute_dict.create_dict()
            # pprint(attributes)
            entities = list(extractor.extract_entities(line))
            pprint(entities)

            params = entities_mul_values(entities, attributes)
            try:
                for att in params[0]:
                    print('value : {}'.format(att))

                for att in params[1]:
                    print('value other : {}'.format(att))
            except:
                print('values are not received')
            print('*' * 40)

        elif 'range' in req_ent_int and len(req_ent_int) == 1:
            ind_attributes = create_attribute_dict.create_indexed_dict()
            attributes = create_attribute_dict.create_dict()
            entities = list(extractor.extract_entities(line))
            pprint(entities)

            params = entities_range(entities, ind_attributes, attributes)
            try:
                for att in params[0]:
                    print('value : {}'.format(att))

                for att in params[1]:
                    print('value other : {}'.format(att))
            except:
                print('values are not received')
            print('*' * 40)

        elif 'value_s' in req_ent_int and len(req_ent_int) == 1:
            entities = list(extractor.extract_entities(line))
            pprint(entities)
            param = entities_value_s(entities)
            try:
                print('var name : {}'.format(param))
            except:
                print('value_s is not received')
            print('*' * 40)

        elif 'value_n' in req_ent_int and len(req_ent_int) == 1:
            entities = list(extractor.extract_entities(line))
            pprint(entities)
            param = entities_value_n(entities)
            try:
                print('value : {}'.format(param))
            except:
                print('value is not received')
            print('*' * 40)

        elif 'var_name' in req_ent_int and 'item' in req_ent_int:
            entities = list(extractor.extract_entities(line, wc='foreach'))
            pprint(entities)
            params = entities_item_varname(entities)
            try:
                print('item : {}'.format(params[0]))
                print('var name : {}'.format(params[1]))
            except:
                print('var_name and item are not received')
            print('*' * 40)

        elif 'var_name' in req_ent_int and 'values' in req_ent_int:
            entities_vn = list(extractor.extract_entities(line, wc='namevalues'))
            entities_val = list(extractor.extract_entities(line))
            pprint(entities_vn)
            pprint(entities_val)
            params = entities_varname_vals(entities_vn, entities_val)
            try:
                print('var name : {}'.format(params[0][0]))
                for p in params[1]:
                    print('value : {}'.format(p))
            except:
                print('var_name and values are not received')
            print('*' * 40)

        elif 'c_value' in req_ent_int and len(req_ent_int) == 1:
            attributes = create_attribute_dict.create_dict()
            entities = list(extractor.extract_entities(line))
            pprint(entities)

            params = entities_mul_values(entities, attributes)
            try:
                for att in params[0]:
                    print('value : {}'.format(att))

                for att in params[1]:
                    print('value other : {}'.format(att))
            except:
                print('class value is not received')
            print('*' * 40)

        if 'var_name' in req_ent_int and 'instance' in req_ent_int:
            entities = list(extractor.extract_entities(line))
            pprint(entities)
            params = entities_varname_instance(entities, req_ent_int)
            try:
                print('var name : {}'.format(params[0]))
                print('value : {}'.format(params[1]))
            except:
                print('var_name and value not received')
            print('*' * 40)

        if 'var_name' in req_ent_int and 's_value' in req_ent_int:
            regex_string = r"\'.*\'"
            string = re.findall(regex_string, line)
            entities = list(extractor.extract_entities(line))
            pprint(entities)
            params = entities_varname(entities)
            try:
                print('var name : {}'.format(params))
                print('value : {}'.format(string))
            except:
                print('var_name is not received')
            print('*' * 40)
    end = time.time()
    print(end)
    print(end-start)


def entities_varname_value(entities, required_entities):
    var_name = ''
    val = ''
    for rent in required_entities:
        if rent == 'var_name':
            for entity in entities:
                if re.search(regex_var, entity):
                    for token in entity.split():
                        if not re.search(regex_var, token):
                            var_name = token
                elif not re.search(regex_num, entity):
                    var_name = entity

        elif rent == 'value':
            for entity in entities:
                if re.search(regex_num, entity):
                    e = entity.replace(',', '')
                    val = e

    return [var_name, val]


def entities_varname(entities):
    var_name = ''
    ignore = ['list', 'array', 'memory', 'null', 'empty', 'null array', 'empty array', 'null list', 'empty list']
    for entity in entities:
        # if re.search(regex_var, entity) and len(entity.split()) > 1:
        if re.search(regex_var, entity):
            for token in entity.split():
                if not re.search(regex_var, token) and token not in ignore:
                    var_name = token
        elif not re.search(regex_num, entity) and len(entity.split()) == 1 and entity not in ignore:
            if var_name is '':
                var_name = entity

    return var_name


def entities_def_value(entities, def_entities):
    var_name = ''
    for entity in entities:
        entity = entity.replace('=', '').strip()
        if entity in def_entities or entity.lower() in def_entities:
            try:
                var_name = def_entities[entity]
            except:
                var_name = def_entities[entity.lower()]

        elif re.search(regex_import, entity) and len(entity.split()) > 1:
            temp = ''
            for token in entity.split():
                if not re.search(regex_import, token):
                    temp += token + ' '
            print(temp)

            if temp.strip() in def_entities or temp.strip().lower() in def_entities:
                var_name = def_entities[temp.strip()]

    return var_name


def entities_mul_values(entities, mul_attributes):
    values = [[], []]
    for entity in entities:
        entity = entity.replace('=', '').strip()
        if entity in mul_attributes or entity.lower() in mul_attributes:
            try:
                values[0].append(mul_attributes[entity])
            except:
                values[0].append(mul_attributes[entity.lower()])

        elif re.search(regex_features, entity):
            temp = ''
            for token in entity.split():
                if not re.search(regex_features, token):
                    temp += token + ' '
            print(temp)

            if temp.strip() in mul_attributes or temp.strip().lower() in mul_attributes:
                values[0].append(mul_attributes[temp.strip()])

            else:
                if temp is not '':
                    values[1].append(temp)
        else:
            values[1].append(entity)

    return values


def entities_range(entities, indexed_attr, mul_attributes):
    values = [[], []]
    indexes = []
    for entity in entities:
        entity = entity.replace('=', '').strip()
        if entity in indexed_attr or entity.lower() in indexed_attr:
            indexes.append(indexed_attr[entity])

        elif re.search(regex_features, entity):
            temp = ''
            for token in entity.split():
                if not re.search(regex_features, token):
                    temp += token + ' '
            print(temp)

            if temp.strip() in indexed_attr or temp.strip().lower() in indexed_attr:
                indexes.append(indexed_attr[entity])

            else:
                if temp is not '':
                    values[1].append(temp)
        else:
            values[1].append(entity)

    try:
        low = min(indexes)
        high = max(indexes)
        print('min : {}, max : {}'.format(low, high))

        for ind in range(low, high + 1):
            values[0].append(mul_attributes[str(ind)])
    except:
        print('Unable to find indexes')

    return values


def entities_value_s(entities):
    var_name = ''
    ignore = ['import', 'sklearn', 'library', 'display', 'print', 'println']
    for entity in entities:
        if re.search(regex_svalues, entity) and len(entity.split()) > 1:
            for token in entity.split():
                if not re.search(regex_svalues, token) and token not in ignore:
                    var_name = token
        elif not re.search(regex_num, entity) and entity not in ignore:
            var_name = entity

    return var_name


def entities_value_n(entities):
    val = 0
    is_percent = False
    for entity in entities:
        if re.search(regex_num, entity):
            e = entity.replace(',', '')
            val = e

        if entity == '%':
            is_percent = True

    if is_percent:
        return int(val) / 100
    else:
        return val


def entities_item_varname(entities):
    result = []
    regex_for = r"\b(([Ff]or)|([Ee]very)|([Ee]ach)|([Tt]hrough)|([Ll]oop)|([Tt]o))\b"
    regex_in = r"\b(([Ii]n)|([Tt]he)|([Ll]ist))\b"
    for entity in entities:
        try:
            if re.search(regex_for, entity):
                for token in entity.split():
                    if not re.search(regex_for, token):
                        result.append(token)

            elif re.search(regex_in, entity):
                for token in entity.split():
                    if not re.search(regex_in, token):
                        result.append(token)

            else:
                result.append(entity)
        except:
            print('Unable to find item or var_name')

    return result


def entities_varname_vals(vn, val):
    result = [[], []]
    is_varname = False
    regex_vn = r"(\b(([Aa]rray)|([Ii]s)|([Aa])|([Ll]ist)|([Cc]alled)|([Nn]amed)|[Tt]o|\.|([Aa]ppend)|([Ss]tring))\b)|="
    ignore = ['list', 'append']

    for entity in vn:
        try:
            if re.search(regex_vn, entity):
                for token in entity.split():
                    if not re.search(regex_vn, token):
                        result[0].append(token)

        except:
            print('Unable to find var_name')

    for entity in val:
        entity = entity.replace('=', '').strip()
        try:
            for e in entity.split():
                if e in result[0][0] or e in ignore:
                    is_varname = True
            if is_varname is False:
                result[1].append(entity)
            else:
                is_varname = False
        except:
            print('Unable to retrieve values')

    return result


def entities_varname_instance(entities, required_entities):
    var_name = ''
    inst = ''
    temp = []
    regex_inst = r"\b((([Ii]nstantiate)|([Vv]ariable)|([Ii]nstance))\b)"
    for rent in required_entities:
        if rent == 'var_name':
            for entity in entities:
                if re.search(regex_var, entity):
                    for token in entity.split():
                        if not re.search(regex_var, token):
                            var_name = token
                            temp.append(entity)
                # elif not re.search(regex_num, entity):
                #     var_name = entity

        elif rent == 'instance':
            for entity in entities:
                if re.search(regex_inst, entity) and entity not in temp:
                    # inst = ''
                    for token in entity.split():
                        if not re.search(regex_inst, token):
                            inst += ' ' + token

                elif not re.search(regex_inst, entity) and entity not in temp:
                    inst = entity

    return [var_name, inst]


if __name__ == "__main__":
    extract = entity_extractor.Extractor()
    generate_entities(extract, extract.req_ent, extract.def_entities)