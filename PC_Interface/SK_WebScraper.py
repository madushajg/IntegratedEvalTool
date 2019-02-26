import bs4
import requests
import lxml
import html5lib
import pandas as pd
import re
import csv
import pymongo

#Varible and arrays
argument_array = []
argument_desc_array = []
value = []

#get gata from web
algoName = "decision tree (sklearn)"
# res = requests.get('https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html')
# res = requests.get('https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html')
# res = requests.get('https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html#sklearn.neural_network.MLPClassifier')
res = requests.get('https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html#sklearn.tree.DecisionTreeClassifier')
soup = bs4.BeautifulSoup(res.text, 'html5lib')
argument = soup.find('td',class_='field-body')

#Extract arguments
for arg in argument.find_all('strong'):
    argument_array.append(arg.text)

#Extract argument description
for arg in argument.find_all('dd'):
    argument_desc_array.append(arg.text.replace('\n',' ').replace('\t', ''))

#Extract default value with argument
for val in argument.find_all('dt'):
    value.append(val.text)

regex = r"\(default=.*?\)|(default:.*)|(default=.*)|\(default =.*?\)|(default.*)"

default_value = [None] * len(argument_array)

#covert string to bool
def str_to_bool(s):
    if s == 'true':
         return True
    elif s == 'false':
         return False
    else:
         raise ValueError

#Extract default values
for i, val in enumerate(value):
    if(val.count('default')==1):
        temp = re.search(regex, value[i]).group()
        temp = temp.replace('default','').replace('=','').replace('(','').replace(')','').replace(':','').replace("’",'').replace("‘",'').replace(' ','').replace(',','')
        temp = temp.lower()
        try:
            temp = float(temp)
        except:
            pass
        try:
            temp = str_to_bool(temp)
        except:
            pass
        if(temp=='null' or temp=='none' or temp==''):
            temp = None
        default_value[i] = temp

#save data
# df = pd.DataFrame({"Argument" : argument_array, "Description" : argument_desc_array, "Default_value" : default_value})
df = [{"algorithm" :algoName, "data" : {"Argument" : argument_array, "Description" : argument_desc_array, "Default_value" : default_value}}]
obj = df[0]
# df.to_csv("SK_output.csv", index=False, encoding="utf-8" )

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["FYP"]
mycol = mydb["SK"]
mycol.delete_one(obj)
mycol.insert_many(df)
# mycol.remove({})
# mycol.insert_many(df.to_dict('records'))
