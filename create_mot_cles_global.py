
import os
import sys
import json
from collections import Counter


PATH = "/Users/victorguerand/test_Archive/formatage_donnee/Rocard/"

def recupere_data():
    data = []
    list = os.listdir(PATH)
    for l in list:
        with open(PATH + l + '/le_discours.json', 'r') as f:
            new_elt = {}
            obj = json.load(f)
            new_elt['key_words'] = obj['key_words']
            new_elt['latitude'] = obj['latitude']
            new_elt['longitude'] = obj['longitude']
            new_elt['auteur'] = obj['auteur']
            new_elt['date'] = obj['date']
            new_elt['year'] = obj['year']
            data.append(new_elt)
    return data




def main():
    print('\033[92m   {}  \033[0m'.format("salut a tous"))

    data = recupere_data()

    new_data = {}
    for d in data:
        if d['year'] in new_data.keys():
            a = Counter(new_data[d['year']])
            b = Counter(d['key_words'])
            a.update(b)
            new_data[d['year']] = dict(a)
        else:
            new_data[d['year']] = d['key_words']

    print('\n\n\n\n\n')
    print(new_data)

    with open('test', 'w') as outfile:
        json.dump(new_data, outfile)



if __name__ == '__main__':
    main()