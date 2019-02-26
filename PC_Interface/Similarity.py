import spacy
import re
import pandas as pd
from spacy.lang.en.stop_words import STOP_WORDS
import pymongo
import difflib
from collections import Counter
import numpy as np

# pd.set_option('display.max_columns', -1)
pd.set_option('display.max_colwidth', -1)
# pd.set_option('display.max_columns', None)

#Spacy model load
nlp = spacy.load('customModel')
# nlp = spacy.load('en_vectors_web_lg')
# nlp = spacy.load('en_core_web_lg')
nlp_en = spacy.load('en')

#Sequence matiching
def similar(a,b):
    seq = difflib.SequenceMatcher(None, a, b)
    d = seq.ratio()
    return d

#Remove punctuvation and lemmertize
def PAL(string):
    x = re.sub("[^A-Za-z0-9\s]+", " ", string)
    doc_lemmertized = ' '.join([str(t.lemma_) for t in nlp(x)])
    doc_lemmertized = doc_lemmertized.replace('-PRON-', '').replace(' ','')
    doc_lemmertized = doc_lemmertized.lower()
    return nlp(doc_lemmertized)

#Remove unwanted words
def RUW(string):
    x = re.sub("[^A-Za-z0-9\s]+", " ",string)
    y = re.sub("[ ]{2,}"," ",x)
    # print(y)
    doc_lemmertized = ' '.join([str(t.lemma_) for t in nlp(y)])
    doc_lemmertized = doc_lemmertized.replace('-PRON-','')
    # print(doc_lemmertized)
    sentence = nlp_en(doc_lemmertized)
    doc_not_stopword = (' '.join([str(t) for t in sentence if not t.is_stop]))
    doc_not_stopword = doc_not_stopword.lower()
    # print(doc_not_stopword)
    doc_POS_Tagged = nlp(' '.join([str(t) for t in nlp_en(doc_not_stopword) if t.pos_ in ['NOUN', 'PROPN', 'VERB']]))
    # print(doc_POS_Tagged)
    return doc_POS_Tagged

algoName1 = "svm (e1071)" # (svm, knn, ann, decision tree)
algoName2 = "svm (sklearn)" # (svm, knn, ann, decision tree)
lang1 = "R"
lang2 = "Python"

def match():
    r_match_element = []
    sk_match_element = []
    unique_parm_match_element = []
    matched = []

    # MongoDB Connection
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["FYP"]
    if(lang1=="R"):
        R_col = mydb["R"]
    else:
        R_col = mydb["SK"]
    if(lang2=="R"):
        SK_col = mydb["R"]
    else:
        SK_col = mydb["SK"]
    Parm_col = mydb["ML_Parameters"]
    r_parm_ori_df = pd.DataFrame(list(R_col.find()))
    r_parm_df = pd.DataFrame.from_dict(r_parm_ori_df['data'][r_parm_ori_df.loc[r_parm_ori_df['algorithm'] == algoName1].index[0]])
    # r_parm_df = r_parm_df.drop(['_id'], axis=1)
    sk_parm_ori_df = pd.DataFrame(list(SK_col.find()))
    sk_parm_df = pd.DataFrame.from_dict(sk_parm_ori_df['data'][sk_parm_ori_df.loc[sk_parm_ori_df['algorithm'] == algoName2].index[0]])
    # sk_parm_df = sk_parm_df.drop(['_id'], axis=1)
    unique_parm_df = pd.DataFrame(list(Parm_col.find()))
    unique_parm_df = pd.DataFrame({"Argument": unique_parm_df['Parameters'][3], "Description": unique_parm_df['Description'][3]})
    R_col_real = mydb["R"]
    SK_col_real = mydb["SK"]
    r_parm_ori_real_df = pd.DataFrame(list(R_col_real.find()))
    sk_parm_ori_real_df = pd.DataFrame(list(SK_col_real.find()))


    # Remove unwanted characters
    def RUC(string):
        x = re.sub("[^A-Za-z0-9\s]+", "", string).lower()
        return x

    # Select perfectly Match parmeters by argument name
    for i, val1 in enumerate(r_parm_df['Argument']):
        for j, val2 in enumerate(sk_parm_df['Argument']):
            # if(val1.lower()==val2.lower()):
            if (RUC(val1) == RUC(val2)):
                r_match_element.append(i)
                sk_match_element.append(j)
                # print(val1)
                for k, val3 in enumerate(unique_parm_df['Argument']):
                    if (val1.lower() == val3.lower()):
                        unique_parm_match_element.append(k)

    # Create dataframe for perfecly match parameters
    perfcMatch_R_df = r_parm_df.loc[r_match_element]
    perfcMatch_R_df = perfcMatch_R_df.reset_index(drop=True)
    perfcMatch_SK_df = sk_parm_df.loc[sk_match_element]
    perfcMatch_SK_df = perfcMatch_SK_df.reset_index(drop=True)

    # Remove perfectly match parameters from comparision
    r_parm_df = r_parm_df.drop(r_match_element)
    r_parm_df = r_parm_df.reset_index(drop=True)
    sk_parm_df = sk_parm_df.drop(sk_match_element)
    sk_parm_df = sk_parm_df.reset_index(drop=True)
    unique_parm_df = unique_parm_df.drop(unique_parm_match_element)
    unique_parm_df = unique_parm_df.reset_index(drop=True)

    # identify na.action, x, y,formula when R and sklearn comparision
    if (lang1 != lang2):
        if(lang1=="R"):
            needToRemove = list(np.where(r_parm_df["Argument"] == 'na.action')[0]) + list(
                np.where(r_parm_df["Argument"] == 'x')[0]) + list(np.where(r_parm_df["Argument"] == 'y')[0])
            notCompare_R_df = r_parm_df.loc[needToRemove]
            notCompare_R_df = notCompare_R_df.reset_index(drop=True)
            r_parm_df = r_parm_df.drop(needToRemove)
            r_parm_df = r_parm_df.reset_index(drop=True)
        else:
            needToRemove = list(np.where(sk_parm_df["Argument"] == 'na.action')[0]) + list(
                np.where(sk_parm_df["Argument"] == 'x')[0]) + list(np.where(sk_parm_df["Argument"] == 'y')[0])
            notCompare_R_df = sk_parm_df.loc[needToRemove]
            notCompare_R_df = notCompare_R_df.reset_index(drop=True)
            sk_parm_df = sk_parm_df.drop(needToRemove)
            sk_parm_df = sk_parm_df.reset_index(drop=True)


    #identify parm_df1 & parm_df2 languge
    if (lang1==lang2 and lang1=="R"):
        libaryName1 = "R"
        libaryName2 = "R"
    elif(lang1==lang2 and lang1=="Python"):
        libaryName1 = "Python"
        libaryName2 = "Python"
    elif(lang1=="R" and (len(sk_parm_df) <= len(r_parm_df))):
        libaryName1 = "Python"
        libaryName2 = "R"
    elif(lang1=="R" and (len(sk_parm_df) >= len(r_parm_df))):
        libaryName1 = "R"
        libaryName2 = "Python"
    elif(lang1=="Python" and (len(sk_parm_df) <= len(r_parm_df))):
        libaryName1 = "R"
        libaryName2 = "Python"
    else:
        libaryName1 = "Python"
        libaryName2 = "R"

    # Find smallest tupled dataframe
    parm_df1 = ''
    parm_df2 = ''
    if (len(sk_parm_df) <= len(r_parm_df)):
        parm_df1 = sk_parm_df
        parm_df2 = r_parm_df
        perfcMatch_df = pd.DataFrame(
            {"Argument_1": perfcMatch_SK_df['Argument'], "Description_1": perfcMatch_SK_df['Description'],
             "Default_value_1": perfcMatch_SK_df['Default_value'], "Argument_2": perfcMatch_R_df['Argument'],
             "Description_2": perfcMatch_R_df['Description'], "Default_value_2": perfcMatch_R_df['Default_value']})
    else:
        parm_df1 = r_parm_df
        parm_df2 = sk_parm_df
        perfcMatch_df = pd.DataFrame(
            {"Argument_1": perfcMatch_R_df['Argument'], "Description_1": perfcMatch_R_df['Description'],
             "Default_value_1": perfcMatch_R_df['Default_value'], "Argument_2": perfcMatch_SK_df['Argument'],
             "Description_2": perfcMatch_SK_df['Description'], "Default_value_2": perfcMatch_SK_df['Default_value']})

    perfcMatch_df["score_arg"] = 'NaN'
    perfcMatch_df["score_desc"] = 'NaN'
    perfcMatch_df["score_val"] = 'NaN'
    perfcMatch_df["total_score"] = 'NaN'
    line1 = len(perfcMatch_df["Argument_1"])

    #Get similarity by differnt scores
    for i, val1 in enumerate(parm_df1['Description']):
        total_score_max = 0.0
        score_arg_max = 0.0
        score_desc_max= 0.0
        score_val_max = 0.0
        similar_arg_no = -2
        for j, val2 in enumerate(parm_df2['Description']):
            # score_arg = 0.0
            score_arg = similar(str(PAL(parm_df1['Argument'][i])),str(PAL(parm_df2['Argument'][j])))
            score_desc = RUW(val1).similarity(RUW(val2))
            score_val = 0.0
            if(parm_df1['Default_value'][i]!=None and parm_df2['Default_value'][j]!=None):
                if(type(parm_df1['Default_value'][i])==str and parm_df1['Default_value'][i]==parm_df2['Default_value'][j]):
                    score_val = 1.0
                elif(parm_df1['Default_value'][i]==parm_df2['Default_value'][j]):
                    score_val = 0.7
                elif(type(parm_df1['Default_value'][i])==type(parm_df2['Default_value'][j])):
                    score_val = 0.3

            #     score_val = PAL(parm_df1['Default_value'][i]).similarity(PAL(parm_df2['Default_value'][j]))
            # print(score_val)
            total_score = score_desc*3 + score_arg*2 + score_val*1
            if(score_desc_max<score_desc):
                score_desc_max = score_desc
            if (score_arg_max < score_arg):
                score_arg_max = score_arg
            if (score_val_max < score_val):
                score_val_max = score_val
            if(total_score_max<total_score):
                total_score_max = total_score
                similar_arg_no = j
            # print(str(parm_df1['Argument'][i])+' '+str(score_desc)+' '+str(score_arg)+' '+str(parm_df2['Argument'][j])+' '+str(total_score))
        if (total_score_max >= 3.75):
        # if(score_desc_max>=0.83 and total_score_max>=1.25):
        # if (score_desc_max >= 0.73 and total_score_max >= 1.15):
            # print(str(parm_df1['Argument'][i])+' '+str(total_score_max)+' '+str(parm_df2['Argument'][similar_arg_no]))
            matched.append([parm_df1['Argument'][i],parm_df1['Description'][i],parm_df1['Default_value'][i],parm_df2['Argument'][similar_arg_no],parm_df2['Description'][similar_arg_no],parm_df2['Default_value'][similar_arg_no],score_arg_max,score_desc_max,score_val_max,total_score_max])

    matched_df = pd.DataFrame(matched,columns=['Argument_1','Description_1','Default_value_1','Argument_2','Description_2','Default_value_2','score_arg','score_desc','score_val','total_score'])
    c = Counter(matched_df['Argument_2'])


    #Remove duplicate matche by higher total score
    for val in set(matched_df['Argument_2']):
        if c[val] > 1:
            select = matched_df.loc[matched_df['Argument_2'] == val]
            max = select['total_score'].idxmax()
            select = select.drop(max)
            matched_df = matched_df.drop(select.index.values)

    #sort according to 'total_score' column
    matched_df= matched_df.sort_values('total_score',ascending=False)

    #Select perfectMatch and Match arguments
    allMatch_df = pd.concat([perfcMatch_df,matched_df])
    allMatch_df = allMatch_df.reset_index(drop=True)
    line2 = len(allMatch_df["Argument_1"])

    #Select not matched arguments
    notMatchTemp_df1 = parm_df1.copy()
    notMatchTemp_df2 = parm_df2.copy()
    for val in allMatch_df['Argument_1']:
        indexNames = notMatchTemp_df1[notMatchTemp_df1['Argument'] == val].index
        notMatchTemp_df1.drop(indexNames, inplace=True)
    for val in allMatch_df['Argument_2']:
        indexNames = notMatchTemp_df2[notMatchTemp_df2['Argument'] == val].index
        notMatchTemp_df2.drop(indexNames, inplace=True)
    if(lang1!=lang2):
        if(libaryName1=="R"):
            notMatchTemp_df1 = pd.concat([notMatchTemp_df1,notCompare_R_df])
            notMatchTemp_df1 = notMatchTemp_df1.reset_index(drop=True)
        else:
            notMatchTemp_df2 = pd.concat([notMatchTemp_df2, notCompare_R_df])
            notMatchTemp_df2 = notMatchTemp_df2.reset_index(drop=True)

    notMatch_df1 = pd.DataFrame({"Argument_1" : notMatchTemp_df1['Argument'], "Description_1" : notMatchTemp_df1['Description'], "Default_value_1" : notMatchTemp_df1['Default_value']})
    notMatch_df1 = notMatch_df1.reset_index(drop=True)
    notMatch_df2 = pd.DataFrame({"Argument_2" : notMatchTemp_df2['Argument'], "Description_2" : notMatchTemp_df2['Description'], "Default_value_2" : notMatchTemp_df2['Default_value']})
    notMatch_df2 = notMatch_df2.reset_index(drop=True)
    notMatch_df = pd.concat([notMatch_df1,notMatch_df2], axis=1)
    notMatch_df["score_arg"] = 'NaN'
    notMatch_df["score_desc"] = 'NaN'
    notMatch_df["score_val"] = 'NaN'
    notMatch_df["total_score"] = 'NaN'

    #Final Result
    result = pd.concat([allMatch_df,notMatch_df])
    result = result.reset_index(drop=True)
    result.columns = ['Argument', 'Description', 'Default_value','Argument', 'Description', 'Default_value','Arg_Similarity','Desc_Similarity','val_Similarity','Total_Similarity']

    # result = result.style.set_table_styles(style.styles)
    # result = result.render()

    return result,line1,line2,libaryName1,libaryName2,r_parm_ori_real_df,sk_parm_ori_real_df



