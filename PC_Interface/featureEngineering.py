import pandas as pd
import numpy as np
import re
from sklearn import preprocessing
from sklearn.preprocessing import Imputer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler
from scipy import stats
import os
import time
import spacy
import json

pd.set_option('display.max_columns', None)

try:
    with open('wildcard.json') as f:
        wildcard = json.load(f)
except:
    print("wildcard not found")

features = []
del_features = []

try:
    features = wildcard['FEATURE_SET']
except:
    pass
try:
    del_features = wildcard['ATTRIBUTES']
except:
    pass


# datasetName = 'who_suicide_statistics'
# classVarible = "sex"
datasetName = wildcard['DATASET']
classVarible = wildcard['TARGET_CLASS']
print(datasetName)

path = "Feature_Engineering_output/"+datasetName+"/"

numANDcat_df = pd.read_csv('Resources/'+datasetName+'',encoding = "iso-8859-1")

drop_col_by_user = []
allCol = []
for col in numANDcat_df.columns.values:
    allCol.append(col)

if (len(features)>0):
    atleastOne =False
    for col in features:
        try:
            allCol.remove(col)
            atleastOne =True
        except:
            pass
    if(atleastOne):
        drop_col_by_user = allCol

if len(del_features)>0:
    drop_col_by_user = del_features

print(drop_col_by_user)
try:
    numANDcat_df = numANDcat_df.drop(drop_col_by_user, axis=1)
except:
    pass


try:
    os.mkdir(path)
except OSError:
    print ("Creation of the directory %s failed" % path)
    print()
else:
    print ("Successfully created the directory %s " % path)
    print()

nlp = spacy.load('en')

def isplural(word):
    nlp_word = nlp(word)
    plural = False
    if nlp_word[0].tag_=='NNS':
        plural = True
    return plural

def binarizing(df,col_name,separator):
    dummies = df[col_name].str.lower()
    dummies = pd.DataFrame({col_name:dummies.values})
    dummies = dummies[col_name].str.replace(' ', '')
    dummies = pd.DataFrame({col_name:dummies.values})
    dummies = dummies[col_name].str.get_dummies(sep=separator)
    dummies = dummies.groupby(dummies.columns, axis=1).sum()
    df = df.drop([col_name], axis=1)
    buinarized_df = pd.concat([df, dummies], axis=1, join_axes=[df.index])
    return buinarized_df

def convertDateTime(col):
    notDateCount = 0
    notDateElement = []
    for i,val in enumerate(numANDcat_df[col]):
        # print(str(i)+' '+str(val))
        try:
            pd.to_datetime(val)
        except:
            notDateCount = notDateCount+1
            notDateElement.append(i)

    persentage = (notDateCount/numANDcat_df[col].count())*100
    if persentage<5:
        for no in notDateElement:
            numANDcat_df.at[no, col] = np.nan
        numANDcat_df[col] = pd.to_datetime(numANDcat_df[col])

def numerization(col):
    strElementCount = 0
    strElement = []
    for i,val in enumerate(numANDcat_df[col]):
        try:
            float(val)
        except:
            strElementCount = strElementCount + 1
            strElement.append(i)
    persentage = (strElementCount/numANDcat_df[col].count())*100
    if persentage<5:
        for no in strElement:
            numANDcat_df.at[no, col] = re.sub('[^0-9.]+','',numANDcat_df[col][no])
        try:
            numANDcat_df[col] = pd.to_numeric(numANDcat_df[col])
        except:
            pass

def removePlusOfNumber(col):
    plusCount = 0
    for val in numANDcat_df[col]:
        try:
            if re.search('(?<=\d)\+',val):
                plusCount = plusCount + 1
        except:
            pass
    persentage = (plusCount/numANDcat_df[col].count())*100
    if persentage>95:
        for i,val in enumerate(numANDcat_df[col]):
            try:
                numANDcat_df.at[i, col] = re.sub('((?<=\d)\+)|(,)|(\D)','',numANDcat_df[col][i])
            except:
                break
        try:
            numANDcat_df[col] = pd.to_numeric(numANDcat_df[col])
        except:
            pass

def lebleEncorder(column):
    le = preprocessing.LabelEncoder()
    le.fit(numANDcat_df[column].astype(str))
    numANDcat_df[column] = le.transform(numANDcat_df[column].astype(str))

print("Start feature engineering")

#Remove columns unique value is 1
uniques = numANDcat_df.apply(lambda x: x.nunique())
numANDcat_df = numANDcat_df.drop(uniques[uniques==1].index, axis=1)
print("Uniqueness 1 columns")
print(uniques[uniques==1].index)
print()

#Find multivaled attributs
print("Finding multiValued attributes")
start = time.clock()
pluralColumns = []
multValueColumns = []

for nn in numANDcat_df.columns.values:
    plural = isplural(nn.lower())
    if(plural==True):
        pluralColumns.append(nn)

separator = []
for pluralCol in pluralColumns:
    for val in numANDcat_df[pluralCol]:
        if(type(val)==str):
            if(val.count(';')>0):
                multValueColumns.append(pluralCol)
                separator.append(";")
                break
            if ((val.count(',')>0) and (re.search('(\,\d{3})', str(val))==None)):
            # if (val.count(',') > 0):
                multValueColumns.append(pluralCol)
                separator.append(",")
                break

if(len(multValueColumns)!=0):
    print("Multivalued attribte founded!  Colomn names="+str(multValueColumns)+"  separators="+str(separator))
    for i,mul_col in enumerate(multValueColumns):
        numANDcat_df = binarizing(numANDcat_df,mul_col,separator[i])
    numANDcat_df.to_csv("Feature_Engineering_output/"+datasetName+"/1_dummy.csv", index=False, encoding="iso-8859-1" )
print(round((time.clock() - start)/60,4))
print()

#numarize data set
print("numerizing")
start = time.clock()
for col in numANDcat_df.columns:
    numerization(col)
print(round((time.clock() - start)/60,4))
print()

#plus remove
print("Removing plus charcters")
start = time.clock()
for col in numANDcat_df.columns:
    removePlusOfNumber(col)
print(round((time.clock() - start)/60,4))
print()

#covenvert date time colomns to relavant format
# print("identifing date columns")
# start = time.clock()
# isTemporal = False
# for col in numANDcat_df.columns:
#     if numANDcat_df[col].dtype == 'object':
#         try:
#             numANDcat_df[col] = pd.to_datetime(numANDcat_df[col])
#             isTemporal = True
#         except ValueError:
#             pass
# if(isTemporal==False):
#     for col,type in enumerate(numANDcat_df.dtypes):
#         if(type==object):
#             convertDateTime(numANDcat_df.columns[col])
# print(round((time.clock() - start)/60,4))
# print()

colomnDataTypes = numANDcat_df.dtypes
# print(colomnDataTypes)

numCol = []
catCol = []
for col in numANDcat_df.columns:
    if (numANDcat_df[col].dtype == 'float64')or(numANDcat_df[col].dtype == 'int64'):
        numCol.append(col)
for col in numANDcat_df.columns:
    if (numANDcat_df[col].dtype == 'object'):
        catCol.append(col)

#use label encoder
print("LableEncording")
start = time.clock()
encordedCol = []
for col,type in enumerate(numANDcat_df.dtypes):
    if ((type == object) or (type == bool)):
        lebleEncorder(numANDcat_df.columns[col])
        encordedCol.append(numANDcat_df.columns[col])
if(len(encordedCol)>0):
    print("Encorded Columns")
    print(encordedCol)
    numANDcat_df.to_csv("Feature_Engineering_output/"+datasetName+"/2_encorded.csv", index=False, encoding="iso-8859-1" )
print(round((time.clock() - start)/60,4))
print()


#find duplicate rows
print('Finding & deleting duplicate rows')
start = time.clock()
dup_temp = numANDcat_df.duplicated()
duplicate_row = []
for i,val in enumerate(dup_temp):
    if(val==True):
        duplicate_row.append(i)
numANDcat_df = numANDcat_df.drop(duplicate_row)
numANDcat_df = numANDcat_df.reset_index(drop=True)

#delete date colomns
dateColumns = []
for col,type in enumerate(numANDcat_df.dtypes):
    if re.search('datetime',str(type)):
        dateColumns.append(numANDcat_df.columns[col])
numANDcat_df = numANDcat_df.drop(dateColumns, axis=1)
print(round((time.clock() - start)/60,4))
print()

temporal = False

for type in numANDcat_df.dtypes:
    if re.search('datetime',str(type)):
        temporal = True
        break

if(temporal==True):
    numANDcat_df.to_csv("Feature_Engineering_output/"+datasetName+"/3_encordedWithoutDateCol.csv", index=False, encoding="iso-8859-1" )

# Find empty cells , colomn wise
print("Finding & filling empty cells")
start = time.clock()
empty_tp = np.where(pd.isnull(numANDcat_df))
empty=[]
emptyAll =[]
for i in numANDcat_df.columns:
    empty.append([])
for i,val in enumerate(empty_tp[1]):
    empty[val].append(empty_tp[0][i])
    emptyAll.append(empty_tp[0][i])

#fix empty cell
numANDcat_df = numANDcat_df.dropna(subset=catCol)
numANDcat_df = numANDcat_df.reset_index(drop=True)

if (temporal):
    numANDcat_df = numANDcat_df.fillna(method='ffill')
else:
    fill_NaN = SimpleImputer(missing_values=np.nan, strategy='mean')
    imputed_DF = pd.DataFrame(fill_NaN.fit_transform(numANDcat_df), columns=numANDcat_df.columns)
    imputed_DF.index = numANDcat_df.index
    numANDcat_df = imputed_DF
numANDcat_df = numANDcat_df.round(2)
if (len(emptyAll)>0):
    numANDcat_df.to_csv("Feature_Engineering_output/"+datasetName+"/4_emptyValueFilled.csv", index=False, encoding="iso-8859-1" )
print(round((time.clock() - start)/60,4))
print("empty cells")
print(empty)
print()

#identify outliers(only apply numerical values)
print("identifing outliers")
start = time.clock()
z = np.abs(stats.zscore(numANDcat_df))
outliers_tp = np.where(z >= 5)
numANDcat_df = numANDcat_df[(z < 5).all(axis=1)]  #delete outliers

outliers=[]
outliersAll=[]
for i in numANDcat_df.columns:
    outliers.append([])
for i,val in enumerate(outliers_tp[1]):
    outliers[val].append(outliers_tp[0][i])
    outliersAll.append(outliers_tp[0][i])

if(len(outliersAll)>0):
    numANDcat_df.to_csv("Feature_Engineering_output/"+datasetName+"/5_outlierRemoved.csv", index=False, encoding="iso-8859-1" )
print(round((time.clock() - start)/60,4))
print("Outliers")
print(outliers)
print()


#Find corelated attribute
print("identifing coralated attributes")
start = time.clock()
corr_matrix=numANDcat_df.corr().abs()  #Compute pairwise correlation of columns (pearson : standard correlation coefficient)
upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool)) # Select upper triangle of correlation matrix
to_drop = [column for column in upper.columns if any(upper[column] > 0.95)] # Find index of feature columns with correlation greater than 0.95
try:
    to_drop.remove(classVarible)
except:
    pass

numANDcat_df = numANDcat_df.drop(to_drop, axis=1)
print(round((time.clock() - start)/60,4))
print('Corelated attributes')
# print(upper)
print(to_drop)
print()
if(len(to_drop)>0):
    numANDcat_df.to_csv("Feature_Engineering_output/"+datasetName+"/6_corelatedAttributeRemoved.csv", index=False, encoding="iso-8859-1" )

#Normalize data set
print("Normalizing")
start = time.clock()
try:
    numCol.remove(classVarible)
except:
    pass
for col in to_drop:
    try:
        numCol.remove(col)
    except:
        pass
normalizedCol = []
for col in numANDcat_df.columns:
    normalizedCol.append(col)
try:
    normalizedCol.remove(classVarible)
except:
    pass
for col in to_drop:
    try:
        normalizedCol.remove(col)
    except:
        pass

scaler = MinMaxScaler()
numANDcat_df[normalizedCol] = scaler.fit_transform(numANDcat_df[normalizedCol])
numANDcat_df = numANDcat_df.round(2)
print(round((time.clock() - start)/60,4))
print("Columns normalize")
print(normalizedCol)
print()

print("PreProccessing Finished")
numANDcat_df.to_csv("Feature_Engineering_output/"+datasetName+"/7_normerlized.csv", index=False, encoding="utf-8")

numANDcat_df.to_csv("Feature_Engineering_output/"+datasetName+"/7_normerlized.csv", index=False, encoding="utf-8")