import re
from pprint import pprint
import os
from google.oauth2 import service_account
import test_detect_intent
from entities import create_attribute_dict, entity_extractor
import time

credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
credentials = service_account.Credentials.from_service_account_file(credentials_path)
PROJECT_ID = os.getenv('GCLOUD_PROJECT')


regex_var = r"\b((([Vv]ariable)|([Nn]ame)|([Ll]ist)|([Aa]rray)|([Ii]mport)|([Uu]se)|([Ii]nstance)|([Mm]odel))\b)|="
regex_num = r"\d+\.?\d*\b"
regex_import = r"\b(([Ii]mport)|([Uu]se)|([Ii]nbuilt)|([Ss]uitable)|([Aa]ppropriate))\b"
regex_features = r"\b(([Cc]olumns)|([Dd]rop)|([Cc]olumn)|([Ff]eatures)|([Ff]eature)|([Aa]ttribute)|([" \
                 r"Nn]ormalization)|([Nn]umerize)|([Uu]se)|([Nn]umerization))\b "
regex_svalues = r"\b(([Ii]mport)|([Ll]ibrary)|([Dd]isplay)|([Pp]rint)|([Pp]rintln))\b"


# method for identifying required entities and call for relevant methods to find them
def generate_entities(extractor, intent, line):
    req_ent = extractor.req_ent
    defined_entities = extractor.def_entities
    intention = intent
    # intention = test_detect_intent.detect_intent_texts(PROJECT_ID, 'df', [line], language_code='en')
    print(intention)
    req_ent_int = req_ent[intention]
    print(req_ent_int)

    # Assign value to float variable, Assign value to integer variable, Define K in KNN
    if 'value' in req_ent_int and 'var_name' in req_ent_int:
        entities_num = list(extractor.extract_entities(line, wc='numbers'))
        entities_vn = list(extractor.extract_entities(line, wc='varname'))
        param_vn = entities_varname_regxep(entities_vn)
        param_value = entities_varname_value(entities_num)
        try:
            print('var name : {}'.format(param_vn[0]))
        except:
            param_vn.append('unknown')
            print('var_name not received')

        try:
            print('value : {}'.format(param_value))
        except:
            param_value.append('unknown')
            print('value not received')
        print('*' * 40)
        return [param_vn[0], param_value]

    # Intentions which are not required any entity
    elif 'N' in req_ent_int:
        print('No need of entity')
        print('*' * 40)

    # Define a variable, Define an array
    elif 'var_name' in req_ent_int and len(req_ent_int) == 1:
        entities_r = list(extractor.extract_entities(line, wc='varname'))
        pprint(entities_r)
        param = entities_varname_regxep(entities_r)
        try:
            print('var name : {}'.format(param[0]))
        except:
            param.append('unknown')
            print('var_name is not received')
        print('*' * 40)
        return [param[0]]

    # Predict clf
    elif 'var_name_clf' in req_ent_int and len(req_ent_int) == 1:
        entities = list(extractor.extract_entities(line, wc='clf'))
        pprint(entities)
        param = entities_varname(entities)
        try:
            print('var name : {}'.format(param[0]))
        except:
            param.append('unknown')
            print('var_name is not received')
        print('*' * 40)
        return [param[0]]

    # Define Language, Algo, DML, MDO, import ML Library, Replace NaN, import ML Algo
    elif 'def_value' in req_ent_int and len(req_ent_int) == 1:
        entities = list(extractor.extract_entities(line))
        pprint(entities)
        param = entities_def_value(entities, defined_entities)
        try:
            print('var name : {}'.format(param))
        except:
            param.append('unknown')
            print('var_name is not received')
        print('*' * 40)
        return [param]

    # drop columns, define features, numerize/ normalize (specific)
    elif 'mul_values' in req_ent_int and len(req_ent_int) == 1:
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
            params.append('unknown')
            print('values are not received')
        print('*' * 40)
        return [params[0]]

    # Drop columns - Range
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
            params.append('unknown')
            print('values are not received')
        print('*' * 40)
        return [params[0]]

    # Print, Import specific modules
    elif 'value_s' in req_ent_int and len(req_ent_int) == 1:
        entities = list(extractor.extract_entities(line))
        pprint(entities)
        param = entities_value_s(entities)
        try:
            print('value : {}'.format(param))
        except:
            param.append('unknown')
            print('value_s is not received')
        print('*' * 40)
        return [param]

    # Split Dataset – Test, Split Dataset – Train
    elif 'value_n' in req_ent_int and len(req_ent_int) == 1:
        # entities = list(extractor.extract_entities(line))
        entities = list(extractor.extract_entities(line, wc='percetages'))
        pprint(entities)
        param = entities_value_n(entities)
        try:
            print('value : {}'.format(param))
        except:
            param.append('unknown')
            print('value is not received')
        print('*' * 40)
        return [param]

    # For each loop
    elif 'var_name' in req_ent_int and 'item' in req_ent_int:
        entities = list(extractor.extract_entities(line, wc='foreach'))
        pprint(entities)
        params = entities_item_varname(entities)
        try:
            print('item : {}'.format(params[0]))
        except:
            params.append('unknown')
            print('var_name is not received')

        try:
            print('var name : {}'.format(params[1]))
        except:
            params.append('unknown')
            print('item is not received')
        print('*' * 40)
        return [params[0], params[1]]

    # Append elements to a list
    elif 'var_name' in req_ent_int and 'values' in req_ent_int:
        entities = list(extractor.extract_entities(line))
        entities_vn = list(extractor.extract_entities(line, wc='varname'))
        param_vn = entities_varname_regxep(entities_vn)
        param_values = entities_vals(entities)
        try:
            print('var name : {}'.format(param_vn[0]))
        except:
            param_vn.append('unknown')
            print('var_name and value not received')

        try:
            for p in param_values:
                if p in param_vn[0]:
                    param_values.remove(p)
                else:
                    print('value : {}'.format(p))
        except:
            param_values.append('unknown')
            print('values not received')
        print('*' * 40)
        return [param_vn[0], param_values]

    # Define Class
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
            params.append('unknown')
            print('class value is not received')
        print('*' * 40)
        return [params[0]]

    # Assign Class instance to variable
    if 'var_name' in req_ent_int and 'instance' in req_ent_int:
        entities = list(extractor.extract_entities(line))
        print(entities)
        entities_vn = list(extractor.extract_entities(line, wc='varname'))
        print(entities_vn)
        param_vn = entities_varname_regxep(entities_vn)
        param_inst = entities_instance(entities)
        try:
            print('var name : {}'.format(param_vn[0]))
        except:
            param_vn.append('unknown')
            print('var_name not received')

        try:
            print('instance : {}'.format(param_inst))
        except:
            param_inst.append('unknown')
            print('instance not received')
        print('*' * 40)
        return [param_vn[0], param_inst]

    # Assign value to string variable
    if 'var_name' in req_ent_int and 's_value' in req_ent_int:
        regex_string = r"\'.*\'"
        string = re.findall(regex_string, line)
        entities = list(extractor.extract_entities(line, wc='varname'))
        pprint(entities)
        params = entities_varname_regxep(entities)
        try:
            print('var name : {}'.format(params[0]))
        except:
            params.append('unknown')
            print('var_name is not received')

        try:
            print('value : {}'.format(string[0]))
        except:
            string.append('unknown')
            print('string is not received')
        print('*' * 40)
        return [params[0], string[0]]


# Assign value to float variable, Assign value to integer variable, Define K in KNN
def entities_varname_value(entities):
    val = ''
    for entity in entities:
        e = entity.replace(',', '')
        val = e

    return val


# Predict clf
def entities_varname(entities):
    result = []
    is_top = False
    regex_vn_top = r"\b(([Ff]or)|([Aa]pply)|([Ii]n)|([Pp]arse)|([Ss]end))\b"
    regex_vn_less = r"\b(([Uu]se)|([Aa]rray)|([Ll]ist))\b"

    for entity in entities:
        try:
            if re.search(regex_vn_top, entity):
                for token in entity.split():
                    if not re.search(regex_vn_top, token) and not re.search(regex_vn_less, token):
                        result.append(token)
                        is_top = True
            elif re.search(regex_vn_less, entity) and is_top is False:
                for token in entity.split():
                    if not re.search(regex_vn_top, token) and not re.search(regex_vn_less, token):
                        result.append(token)
        except:
            print('Unable to find var_name_clf')

    return result


# Define Language, Algo, DML, MDO, import ML Library, Replace NaN, import ML Algo
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


# drop columns, define features, numerize/ normalize (specific)
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


# Drop columns - Range
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


# Print, Import specific modules
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


# Split Dataset – Test, Split Dataset – Train
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


# For each loop
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


# Append elements to a list
def entities_vals(val):
    result = []
    ignorable = False
    ignore = ['list', 'append', 'array', 'values']

    for entity in val:
        entity = entity.replace('=', '').strip()
        try:
            for e in entity.split():
                if e in ignore:
                    ignorable = True
            if ignorable is False:
                result.append(entity)
            else:
                ignorable = False
        except:
            print('Unable to retrieve values')

    return result


# Assign Class instance to variable
def entities_instance(entities):
    inst = ''
    regex_inst = r"\b((([Ii]nstantiate)|([Vv]ariable)|([Ii]nstance)|([Ii]nitiate))\b)"
    instances = ['instantiate', 'variable', 'instance', 'initiate']
    for entity in entities:
        if re.search(regex_inst, entity):
            # inst = ''
            for token in entity.split():
                if token in instances:
                    entity = entity.replace(token, '')
                    inst = entity.strip()

        elif not re.search(regex_inst, entity):
            inst = entity
        else:
            inst = 'undefined'

    return inst


# var name by regexp
def entities_varname_regxep(entities):
    result = []
    is_top = False
    regex_vn_top = r"(\b(([Tt]o)|([Vv]ariable)|([Cc]alled)|([Ii]s)|([Nn]amed)|\.|([Oo]f)|([Aa]s)|([Ll]ist)|([Aa]rray)|([Aa]ppend))\b)|="
    regex_vn_less = r"(\b(([Dd]efine)|([Nn]amed)|([Ss]tring)|([Nn]ull)|([Cc]reate)|([Ss]ubstitute)|([Ww]ith)|([Tt]he)|([Nn]ame)|([Ee]mpty))\b)"

    for entity in entities:
        try:
            if re.search(regex_vn_top, entity):
                for token in entity.split():
                    if not re.search(regex_vn_top, token) and not re.search(regex_vn_less, token):
                        result.append(token)
                        is_top = True
            elif re.search(regex_vn_less, entity) and is_top is False:
                for token in entity.split():
                    if not re.search(regex_vn_top, token) and not re.search(regex_vn_less, token):
                        result.append(token)
        except:
            print('Unable to find var_name')

    return result


