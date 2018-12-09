import os
import json
import sys
from collections import Counter
from nltk import FreqDist
import re
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize

from shutil import copyfile

# copyfile(src, dst)

PATH = "/Users/victorguerand/test_Archive/formatage_donnee"

PATH_TO_DATASET = "/Users/victorguerand/Desktop/03 - Le politique parle au citoyen/Rocard - discours"

sys.path.insert(0, PATH)



def removeStopWords(words):

    data = []
    for w in words:
        if len(w) > 4 and w.isalpha():
            data.append(w)
    return data


def key_word(txt):
    re.sub('[^A-Za-z0-9]+', '', txt)

    txt = txt.split(' ')
    txt = removeStopWords(txt)
    fdist1 = FreqDist(txt)
    print (fdist1.most_common(20))
    return fdist1

def create_mot_clef():
    c = Counter(["hello", "test", "string", "people", "hello", "hello"])
    print(c)


def normalize_path(path):
    path_input = path.replace('\\', '/')
    return path_input


def read_discours(path):
    path = path[2:]
    try:
        with open(PATH_TO_DATASET + path, "r") as file:
            r = file.read()
        return r
    except Exception as e:
        print('\033[93m {} \033[0m'.format(e))


def main():
    print(sys.path)
    print('Running program :\n{}\n'.format(os.path.realpath(__file__)))
    print('\033[92m   {}  \033[0m'.format("salut a tous"))

    with open(PATH + '/Discours.json', 'r') as f:
        obj = json.load(f)

    for el in obj:

        if os.path.isdir(PATH + '/' + el['auteur']) is False:
            print('\033[92m  Directory  {} created  \033[0m'.format(el['auteur']))
            os.mkdir(PATH + '/' + el['auteur'])

        data = el

        if not data['date'] or not data['lieu'] or not data['latitude'] or not data['longitude'] or not data['path']:
            print('\033[93m Warning Empty data \033[0m')
            continue

        data['path'] = normalize_path(data['path'])

        data['text'] = read_discours(data['path'])
        if not data['text']:
            continue
        data['key_words'] = key_word(data['text'])


        if os.path.isdir(PATH + '/' + el['auteur'] + '/' + el['id']) is False:
            print('\033[92m  Directory  {} created  \033[0m'.format(el['auteur'] + '/' + el['id']))
            os.mkdir(PATH + '/' + el['auteur'] + '/' + el['id'])

        with open(PATH + '/' + el['auteur'] + '/' + el['id'] + '/le_discours.json', 'w') as outfile:
            json.dump(data, outfile)

        if os.path.isdir(PATH + '/' + el['auteur'] + '/' + el['id']) is True:
            print('\033[92m  Directory  {} created  \033[0m'.format(el['auteur'] + '/' + el['id']) + '/Images')
            if os.path.isdir(PATH + '/' + el['auteur'] + '/' + el['id'] + '/Images') is False:
                os.mkdir(PATH + '/' + el['auteur'] + '/' + el['id'] + '/Images')




if __name__ == '__main__':
    main()
