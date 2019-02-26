import os
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
# from nltk.tokenize import sent_tokenize
from detect_intent_texts import detect_intent_texts
import os

PROJECT_ID = os.getenv('GCLOUD_PROJECT')
SESSION_ID = 'fake_session_for_testing'

root_path = os.path.normpath(os.getcwd() + os.sep + os.pardir) + '/PC_Interface/Resources'
os.chdir(root_path)

tokenizer = RegexpTokenizer('\s+', gaps=True)
lemmatizer = WordNetLemmatizer()

pc_file = open('pc1', "r")
pc_read = pc_file.read()

lines = pc_read.split('\n')


# lines = sent_tokenize(pc_read, language='english')

def tokenize_text(c_line):
    tknzd_line = tokenizer.tokenize(c_line)
    tokens = [token.lower() for token in tknzd_line]
    return tokens


def lemmatize_tokens(tokens):
    l_tokens = list(())
    for tks in tokens:
        lemma = lemmatizer.lemmatize(tks, pos="v")
        l_tokens.append(lemma)
    return l_tokens


lines = list(filter(None, lines))
print(lines)


def test_detect_intent_texts():
    for line in lines:
        detect_intent_texts(PROJECT_ID, SESSION_ID, line, 'en-US')


if __name__ == '__main__':
    test_detect_intent_texts()
