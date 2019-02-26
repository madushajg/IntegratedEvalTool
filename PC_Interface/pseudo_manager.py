from pprint import pprint

import re

from entities import entity_extraction_app

ds_name = ''


def generate_pseudo_code(response, pseudo_gen):
    idnt_map = pseudo_gen.idnt_map
    query_text = response.query_result.query_text
    intent = response.query_result.intent.display_name
    confidence = response.query_result.intent_detection_confidence
    fulfillment = response.query_result.fulfillment_text
    parameters = dict(response.query_result.parameters)

    print('Query text: {}'.format(query_text))
    print('Detected intent: {} (confidence: {})\n'.format(intent, confidence))
    print('Fulfillment text: {}\n'.format(fulfillment))
    print(parameters)
    wc = pseudo_gen.wildcard

    if idnt_map[intent] == 'N':
        return fulfillment
    elif idnt_map[intent] == 'DF':
        pc = process_df(intent, parameters, pseudo_gen, wc)
        if intent == 'For Loop':
            return pc
        else:
            return fulfillment
    elif idnt_map[intent] == 'ER':
        pc = process_er(query_text, intent, parameters, pseudo_gen, wc)
        return pc

    pprint(wc)


def process_er(query, intent, parameters, pseudo_gen, wild_cd):
    extract = pseudo_gen.extract
    entities_from_er = entity_extraction_app.generate_entities(extract, intent, query)

    if intent == 'Assign value to float variable' or intent == 'Assign value to integer variable' or intent == 'Assign value to String variable':
        var_name = 'VAR' + str(len(pseudo_gen.varn))
        var_val = 'VAR_VALUE' + str(len(pseudo_gen.var_value))
        pseudo_gen.varn.append(var_name)
        pseudo_gen.var_value.append(var_val)
        wild_cd[var_name] = entities_from_er[0]
        wild_cd[var_val] = entities_from_er[1]

        replacements = {'VAR': var_name, 'VAR_VALUE': var_val}

        def replace(match):
            return replacements[match.group(0)]

        pc = re.sub('|'.join(r'\b%s\b' % re.escape(s) for s in replacements), replace, 'define variable VAR and '
                                                                                       'assign VAR_VALUE')
        print(pc)
        return pc

    if intent == 'Define a variable':
        var_name = 'VAR' + str(len(pseudo_gen.varn))
        var_val = 'VAR_VALUE' + str(len(pseudo_gen.var_value))
        pseudo_gen.varn.append(var_name)
        pseudo_gen.var_value.append(var_val)
        wild_cd[var_name] = entities_from_er[0]
        wild_cd[var_val] = 'None'

        replacements = {'VAR': var_name, 'VAR_VALUE': var_val}

        def replace(match):
            return replacements[match.group(0)]

        pc = re.sub('|'.join(r'\b%s\b' % re.escape(s) for s in replacements), replace, 'define variable VAR and assign '
                                                                                       'VAR_VALUE')
        print(pc)
        return pc

    if intent == 'Define an array':
        st_arr = 'STRING_ARRAY' + str(len(pseudo_gen.st_array))
        pseudo_gen.st_array.append(st_arr)
        pseudo_gen.st_values.append('STRING_VALUES' + str(len(pseudo_gen.st_values)))
        wild_cd[st_arr] = entities_from_er[0]

        replacements = {'STRING_ARRAY': st_arr}

        def replace(match):
            return replacements[match.group(0)]

        pc = re.sub('|'.join(r'\b%s\b' % re.escape(s) for s in replacements), replace, 'define empty array '
                                                                                       'STRING_ARRAY')
        print(pc)
        return pc

    if intent == 'Append elements to a list':
        st_arr = 'STRING_ARRAY' + str(len(pseudo_gen.st_array))
        st_val = 'STRING_VALUES' + str(len(pseudo_gen.st_values))
        pseudo_gen.st_array.append(st_arr)
        pseudo_gen.st_values.append(st_val)
        wild_cd[st_arr] = entities_from_er[0]
        wild_cd[st_val] = entities_from_er[1]

        replacements = {'STRING_ARRAY': st_arr, 'STRING_VALUES': st_val}

        def replace(match):
            return replacements[match.group(0)]

        pc = re.sub('|'.join(r'\b%s\b' % re.escape(s) for s in replacements), replace, 'define array STRING_ARRAY '
                                                                                       'with values STRING_VALUES')
        print(pc)
        return pc

    if intent == 'Define Class':
        wild_cd['TARGET_CLASS'] = str(entities_from_er[0][0])
        pc = 'define variable target_class and assign TARGET_CLASS'
        print(pc)
        return pc

    if intent == 'Define features':
        wild_cd['FEATURE_SET'] = entities_from_er[0]
        pc = 'define array features and assign FEATURE_SET'
        print(pc)
        return pc

    if intent == 'Drop columns' or intent == 'Drop columns - Range':
        wild_cd['ATTRIBUTES'] = entities_from_er[0]
        pc = 'drop attributes ATTRIBUTES from dataframe'
        print(pc)
        return pc

    if intent == 'SplitDataset-Test' or intent == 'SplitDataset-Train':
        if intent == 'SplitDataset-Test':
            wild_cd['SPLIT_RATIO'] = 1 - float(entities_from_er[0])
        else:
            wild_cd['SPLIT_RATIO'] = entities_from_er[0]
        pc = 'define variable split and assign SPLIT_RATIO'
        print(pc)
        return pc

    if intent == 'ForEach Loop':
        ele = 'ELEMENT' + str(len(pseudo_gen.element))
        rn_arr = 'RANDOM_LIST' + str(len(pseudo_gen.rn_array))
        pseudo_gen.element.append(ele)
        pseudo_gen.rn_array.append(rn_arr)
        wild_cd[ele] = entities_from_er[0]
        wild_cd[rn_arr] = entities_from_er[1]

        replacements = {'ELEMENT': ele, 'RANDOM_LIST': rn_arr}

        def replace(match):
            return replacements[match.group(0)]

        pc = re.sub('|'.join(r'\b%s\b' % re.escape(s) for s in replacements), replace, 'iterate for each ELEMENT in '
                                                                                       'RANDOM_LIST')
        print(pc)
        return pc

    if intent == 'Assign Class instance to variable':
        vn = entities_from_er[0]
        ins = entities_from_er[1]

        replacements = {'VAR': vn, 'INSTANCE': ins}

        def replace(match):
            return replacements[match.group(0)]

        pc = re.sub('|'.join(r'\b%s\b' % re.escape(s) for s in replacements), replace, 'define variable VAR and '
                                                                                       'assign INSTANCE class')
        print(pc)
        return pc

    if intent == 'Normalization-Specific':
        wild_cd['NORMALIZE'] = entities_from_er[0]

    if intent == 'Numerization-Specific':
        wild_cd['NUMERIZE'] = entities_from_er[0]

    if intent == 'Predict clf':
        wild_cd['PREDICT'] = entities_from_er[0]


def process_df(intent, parameters, pseudo_gen, wild_cd):
    if intent == 'Define K in KNN':
        wild_cd['NEIGHBOURS'] = int(parameters['number-integer'])

    elif intent == 'For Loop':
        num = 'RANDOM_NUMBER' + str(len(pseudo_gen.rn_num))
        pseudo_gen.rn_num.append(num)
        wild_cd[num] = int(parameters['number-integer'])
        return 'iterate for ' + num + 'times'

    if intent == 'Define Algorithm':
        wild_cd['ALGORITHM'] = parameters['Algorithms']

    # elif intent == 'Load dataset':
    #     ds = wild_cd['DATASET']
