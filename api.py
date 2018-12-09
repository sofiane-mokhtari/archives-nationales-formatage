
from flask import Flask, Response, make_response
import json, os
# main application instance
app = Flask(__name__)
from collections import Counter
from PIL import Image


PATH = "/Users/victorguerand/test_Archive/formatage_donnee/Rocard/"


def get_all_key_words():
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

def get_all_discours():
    data = []
    list = os.listdir(PATH)
    for l in list:
        with open(PATH + l + '/le_discours.json', 'r') as f:
            new_elt = {}
            obj = json.load(f)
            data.append(obj)
    return data

def get_list_of_discours():
    data = []
    list = os.listdir(PATH)
    for l in list:
        with open(PATH + l + '/latlong.json', 'r') as f:
            new_elemt = {}
            new_elemt['title'] = l
            new_elemt['latlong'] = json.load(f)
            data.append(new_elemt)
    return data

def get_one_discours(title):
    try:
        with open(PATH + title + '/le_discours.json', 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(e)


def recupere_all_keys_words_by_year():
    """Ex

        "1949" : {
                  ...
                 }
        "1950" : {
                 ...
                }

    """
    data = get_all_key_words()
    new_data = {}
    for d in data:
        if d['year'] in new_data.keys():
            a = Counter(new_data[d['year']])
            b = Counter(d['key_words'])
            a.update(b)
            new_data[d['year']] = dict(a)
        else:
            new_data[d['year']] = d['key_words']
    return new_data


def get_lists_manuscrit(title):
    try:
        list = os.listdir(PATH + title + '/Manuscrits')
        return list
    except Exception as e:
        print(e)
    return None


@app.route("/")
def hello():
    return "Hello World!"

######## GET KEYWORDS ##########

@app.route('/keywords_by_years')
def name_inutile():
    data = recupere_all_keys_words_by_year()
    return Response(response=json.dumps(data), status=200, mimetype='application/json')



####### GET DISCOURS #################

@app.route('/discours_all')
def name_inutile2():
    data = get_all_discours()
    return Response(response=json.dumps(data), status=200, mimetype='application/json')


# @app.route('/discours_by_years')
# def name_inutile5():
#     data =

@app.route('/list_discours')
def name_inutile3():
    data = get_list_of_discours()
    return Response(response=json.dumps(data), status=200, mimetype='application/json')


@app.route('/get_one_discours/<title>')
def name_inutile4(title):
    print("pute")
    # title = "17_10_2011-Antony"
    data = get_one_discours(title)
    return Response(response=json.dumps(data), status=200, mimetype='application/json')

####### GET IMAGES MANUSCRIT #################


@app.route('/lists_manuscrit/<title>')
def inutile_name_fuc(title):
    data = get_lists_manuscrit(title)
    return Response(response=json.dumps(data), status=200, mimetype='application/json')

#
# @app.route('/manuscrits/<title/<name>')
# def get_image(title, name):
#     image_bits = Image.open(PATH + title + "/picture.jpg")
#     response = make_response(image_bits)
#     response.headers.set('Content-Type', 'image/jpeg')
#     response.headers.set('Content-Disposition', 'attachment', filename='{}.jpg'.format(name))
#     return response
#
#
