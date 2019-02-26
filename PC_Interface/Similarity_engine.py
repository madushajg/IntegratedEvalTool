import spacy
import time

# UPLOAD_FOLDER = '/media/madusha/DA0838CA0838A781/PC_Interface/Resources/'
UPLOAD_FOLDER = ' /media/arshad/Data/FYP/FYP/UserSpecs2PseudoCode/PC_Interface'
# /media/arshad/Data/FYP/FYP/UserSpecs2PseudoCode/PC_Interface

class Spacy:
    nlp = spacy.load('en_core_web_lg')
    sim_en_corpus = open('/media/arshad/Data/FYP/FYP/UserSpecs2PseudoCode/PC_Interface/Resources/sim_en_corpus').read()
    intentions = {}

    for i, line in enumerate(sim_en_corpus.split("\n")):
        content = line.split(',')
        text = ''
        for c in content[0:len(content)-1]:
            if text is '':
                text += c.replace('\"', '').rstrip('\"')
            else:
                text += ','+c.replace('\'', '').rstrip('\"')
        try:
            intentions[text] = content[len(content)-1]
        except:
            print("Unable to locate text corpus for SE")

    intents = list(intentions.keys())


c = Spacy()


def find_similar_intent(statement):
    index = 0
    max_similarity = 0
    for i in c.intents:
        similarity = c.nlp(statement).similarity(c.nlp(i))
        if similarity > max_similarity:
            max_similarity = similarity
            index = i

        # print(str(similarity) + "\t" + i)

    # print('Max similarity : ' + c.intentions[index] + '(' + str(max_similarity) + ')')

    return [c.intentions[index], max_similarity]


if __name__ == '__main__':
    start = time.time()
    print(start)
    text = ['ASSIGN 6 TO RT', 'assign value 10 for variable p']
    for t in text:
        print(t)
        print(find_similar_intent(t))
        print('*'*50)
    end = time.time()
    print(end-start)