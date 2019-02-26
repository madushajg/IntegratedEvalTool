from sklearn import model_selection, preprocessing, linear_model, naive_bayes, metrics, svm
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn import decomposition, ensemble
import pandas as pd
import statistics

predicted_vector = []
classes_csv = open('/home/arshad/Documents/FYP99/FYP/UserSpecs2PseudoCode/PC_Interface/pc_corpus/classes.csv').read()
classes = {}

for k, line in enumerate(classes_csv.split("\n")):
    try:
        if line is not '':
            content = line.split(',')
        classes[content[0]] = (content[1])
    except:
        print("Unable to locate classes_csv")


def predict(classifier, feature_vector_train, label, feature_vector_pred, header):
    clf = classifier
    clf.fit(feature_vector_train, label)
    r = clf.predict(feature_vector_pred)
    lbl = encoder.inverse_transform(r)
    # predicted_vector.append(r)
    for lb in lbl:
        intent = classes[lb]
        print(intent)
    predicted_vector.append(str(lbl))
    print("-" * 30)
    print(header + "\n" + str(r) + "-" + str(lbl))
    print("=" * 50)


def train_model(classifier, feature_vector_train, label, feature_vector_valid, is_neural_net=False):
    # fit the training dataset on the classifier
    classifier.fit(feature_vector_train, label)

    # predict the labels on validation dataset
    predictions = classifier.predict(feature_vector_valid)

    if is_neural_net:
        predictions = predictions.argmax(axis=-1)

    return metrics.accuracy_score(predictions, valid_y)


# load the dataset
# data = open('pc_corpus/corpus').read()
data = open('pc_corpus/user_entered').read()
labels, texts = [], []

# load the dataset (testing 1by1)
data_testing = open('pc_corpus/pred')
# data_testing = open('pc_corpus/users_entered_lines')
texts_testing = [line for line in data_testing.readlines() if line.strip()]

# load the dataset (filling 1by1)
data_filling = open('pc_corpus/test_filling').read()
labels_filling, texts_filling = [], []

for i, line in enumerate(data.split("\n")):
    content = line.split()
    try:
        labels.append(content[0])
        texts.append(" ".join(content[1:]))
    except:
        print("End of the list")

for i, line in enumerate(data_filling.split("\n")):
    content = line.split()
    try:
        labels_filling.append(content[0])
        texts_filling.append(" ".join(content[1:]))
    except:
        print("End of the list")

# create a dataframe using texts and lables
trainDF = pd.DataFrame()
trainDF['text'] = texts
trainDF['label'] = labels

# create a dataframe using texts and lables (testing 1by1)
trainDF_testing = pd.DataFrame()
trainDF_testing['text'] = texts_testing
print(trainDF_testing['text'])

# create a dataframe using texts and lables (filling)
trainDF_filling = pd.DataFrame()
trainDF_filling['text'] = texts_filling
trainDF_filling['label'] = labels_filling

# split the dataset into training and validation datasets
train_x, valid_x, train_y, valid_y = model_selection.train_test_split(trainDF['text'], trainDF['label'], test_size=0.2)

# combine the filling and corpus
frames_y = [valid_y, trainDF_filling['label']]
frames_x = [valid_x, trainDF_filling['text']]
valid_y_filled = pd.concat(frames_y)
valid_x_filled = pd.concat(frames_x)
# print(valid_x)
print("=" * 50)
# print(valid_x_filled)

f = open("results.txt", "w+")
f.write('*' * 120 + '\n')

# label encode the target variable
encoder = preprocessing.LabelEncoder()
train_y = encoder.fit_transform(train_y)

f.write('=' * 120 + '\n')
valid_y = encoder.fit_transform(valid_y_filled)

for n in range(48):
    x = encoder.inverse_transform(n)
    f.write(str(n) + " : " + str(x) + "\n")

# create a count vectorizer object
count_vect = CountVectorizer(analyzer='word', token_pattern=r'\w{1,}')
count_vect.fit(pd.concat([trainDF['text'], trainDF_testing['text'], trainDF_filling['text']]))

# transform the training and validation data using count vectorizer object
xtrain_count = count_vect.transform(train_x)
xvalid_count = count_vect.transform(valid_x_filled)
xvalid_count_t = count_vect.transform(trainDF_testing['text'])
# print(xvalid_count_t)

# word level tf-idf
tfidf_vect = TfidfVectorizer(analyzer='word', token_pattern=r'\w{1,}', max_features=5000)
tfidf_vect.fit(pd.concat([trainDF['text'], trainDF_testing['text'], trainDF_filling['text']]))
xtrain_tfidf = tfidf_vect.transform(train_x)
xvalid_tfidf = tfidf_vect.transform(valid_x_filled)
xvalid_tfidf_t = tfidf_vect.transform(trainDF_testing['text'])

# ngram level tf-idf
tfidf_vect_ngram = TfidfVectorizer(analyzer='word', token_pattern=r'\w{1,}', ngram_range=(2, 3), max_features=5000)
tfidf_vect_ngram.fit(pd.concat([trainDF['text'], trainDF_testing['text'], trainDF_filling['text']]))
xtrain_tfidf_ngram = tfidf_vect_ngram.transform(train_x)
xvalid_tfidf_ngram = tfidf_vect_ngram.transform(valid_x_filled)
xvalid_tfidf_ngram_t = tfidf_vect_ngram.transform(trainDF_testing['text'])

# characters level tf-idf
tfidf_vect_ngram_chars = TfidfVectorizer(analyzer='char', token_pattern=r'\w{1,}', ngram_range=(2, 3),
                                         max_features=5000)
tfidf_vect_ngram_chars.fit(pd.concat([trainDF['text'], trainDF_testing['text'], trainDF_filling['text']]))
xtrain_tfidf_ngram_chars = tfidf_vect_ngram_chars.transform(train_x)
xvalid_tfidf_ngram_chars = tfidf_vect_ngram_chars.transform(valid_x_filled)
xvalid_tfidf_ngram_chars_t = tfidf_vect_ngram_chars.transform(trainDF_testing['text'])

predict(svm.SVC(gamma=0.001, C=100.), xtrain_count, train_y, xvalid_count_t, "SVM, N-Gram Vectors")
predict(naive_bayes.MultinomialNB(), xtrain_count, train_y, xvalid_count_t, "NB, Count Vectors")
predict(naive_bayes.MultinomialNB(), xtrain_tfidf, train_y, xvalid_tfidf_t, "NB, WordLevel TF-IDF")
predict(naive_bayes.MultinomialNB(), xtrain_tfidf_ngram, train_y, xvalid_tfidf_ngram_t, "NB, N-Gram Vectors")
predict(naive_bayes.MultinomialNB(), xtrain_tfidf_ngram_chars, train_y, xvalid_tfidf_ngram_chars_t, "NB, CharLevel "
                                                                                                    "Vectors")

predict(linear_model.LogisticRegression(), xtrain_count, train_y, xvalid_count_t, "LR, Count Vectors")
predict(linear_model.LogisticRegression(), xtrain_tfidf, train_y, xvalid_tfidf_t, "LR, WordLevel TF-IDF")
predict(linear_model.LogisticRegression(), xtrain_tfidf_ngram, train_y, xvalid_tfidf_ngram_t, "LR, N-Gram Vectors")
predict(linear_model.LogisticRegression(), xtrain_tfidf_ngram_chars, train_y, xvalid_tfidf_ngram_chars_t, "LR, "
                                                                                                          "CharLevel "
                                                                                                          "Vectors")
predict(svm.SVC(), xtrain_tfidf_ngram, train_y, xvalid_tfidf_ngram_t, "SVM, N-Gram Vectors")
predict(ensemble.RandomForestClassifier(), xtrain_count, train_y, xvalid_count_t, "RF, Count Vectors")
predict(ensemble.RandomForestClassifier(), xtrain_tfidf, train_y, xvalid_tfidf_t, "RF, WordLevel TF-IDF")

# Naive Bayes on Count Vectors
accuracy = train_model(naive_bayes.MultinomialNB(), xtrain_count, train_y, xvalid_count)
print("NB, Count Vectors: ", accuracy)

# Naive Bayes on Word Level TF IDF Vectors
accuracy = train_model(naive_bayes.MultinomialNB(), xtrain_tfidf, train_y, xvalid_tfidf)
print("NB, WordLevel TF-IDF: ", accuracy)

# Naive Bayes on Ngram Level TF IDF Vectors
accuracy = train_model(naive_bayes.MultinomialNB(), xtrain_tfidf_ngram, train_y, xvalid_tfidf_ngram)
print("NB, N-Gram Vectors: ", accuracy)

# Naive Bayes on Character Level TF IDF Vectors
accuracy = train_model(naive_bayes.MultinomialNB(), xtrain_tfidf_ngram_chars, train_y, xvalid_tfidf_ngram_chars)
print("NB, CharLevel Vectors: ", accuracy)

# Linear Classifier on Count Vectors
accuracy = train_model(linear_model.LogisticRegression(), xtrain_count, train_y, xvalid_count)
print("LR, Count Vectors: ", accuracy)

# Linear Classifier on Word Level TF IDF Vectors
accuracy = train_model(linear_model.LogisticRegression(), xtrain_tfidf, train_y, xvalid_tfidf)
print("LR, WordLevel TF-IDF: ", accuracy)

# Linear Classifier on Ngram Level TF IDF Vectors
accuracy = train_model(linear_model.LogisticRegression(), xtrain_tfidf_ngram, train_y, xvalid_tfidf_ngram)
print("LR, N-Gram Vectors: ", accuracy)

# Linear Classifier on Character Level TF IDF Vectors
accuracy = train_model(linear_model.LogisticRegression(), xtrain_tfidf_ngram_chars, train_y, xvalid_tfidf_ngram_chars)
print("LR, CharLevel Vectors: ", accuracy)

# SVM on Ngram Level TF IDF Vectors
accuracy = train_model(svm.SVC(), xtrain_tfidf_ngram, train_y, xvalid_tfidf_ngram)
print("SVM, N-Gram Vectors: ", accuracy)

# SVM on Ngram Level TF IDF Vectors (param changed)
accuracy = train_model(svm.SVC(gamma=0.001, C=100.), xtrain_count, train_y, xvalid_count)
print("SVM, N-Gram Vectors Mod: ", accuracy)

# RF on Count Vectors
accuracy = train_model(ensemble.RandomForestClassifier(), xtrain_count, train_y, xvalid_count)
print("RF, Count Vectors: ", accuracy)

# RF on Word Level TF IDF Vectors
accuracy = train_model(ensemble.RandomForestClassifier(), xtrain_tfidf, train_y, xvalid_tfidf)
print("RF, WordLevel TF-IDF: ", accuracy)

# print(predicted_vector)

# for i in predicted_vector:
#     print(encoder.inverse_transform())

try:
    res = statistics.mode(predicted_vector)
except statistics.StatisticsError:
    print('equal no of res found')
    res = predicted_vector[6]

# print(res.split())
for result in res.split():
    result = result.replace(']', '').replace('[','').replace('\'', '')
    i = classes[result]
    print(i)

