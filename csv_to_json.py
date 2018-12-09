import csv, json
import unicodedata
import requests

PATH = '/Users/victorguerand/test_Archive/formatage_donnee/03_le_politique_parle_au_citoyen/Rocard - Allocutions - Inventaire/FRAN_IR_050330_Rocard_allocutions.csv'

PATH_PHOTO = '/Users/victorguerand/test_Archive/formatage_donnee/03_le_politique_parle_au_citoyen/Rocard - Reportages photographiques - Inventaire/rocard_FRAN_IR_050535_photos.csv'


# PATH = 'C:\\Users\\sofia\\Desktop\\formatage_donnee\\03_le_politique_parle_au_citoyen\\Rocard - Allocutions - Inventaire/FRAN_IR_050330_Rocard_allocutions.csv'

# PATH_PHOTO = 'C:\\Users\\sofia\\Desktop\\formatage_donnee\\03_le_politique_parle_au_citoyen\\Rocard - Reportages photographiques - Inventaire/rocard_FRAN_IR_050535_photos.csv'

def save_new_json(name, value):
    print('done')
    with open(name, 'w', encoding='utf8') as outfile:
        json.dump(value, outfile)


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])


def parse_premier(str):
    if str == "1er":
        return "01"
    if len(str) > 2:
        return str.split('-')[1]
    return str


def replace_recards_to_recards(path):
    path.replace("Rocards", "Rocard")
    return path


def create_json_discours():
    data = []
    csv_read = []
    with open(PATH, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        for row in spamreader:
            csv_read.append(row)
    i = 0
    print(spamreader)
    for row in csv_read:
        lieux = remove_accents((row[5].split(","))[0])
        if ("S. l." in lieux or lieux == " "):
            continue
        else:
            departement = lieux.split('(')
            if (len(departement) == 2):
                lieux = departement[0][:-1]
            if len(lieux) and lieux[0] == '[':
                lieux = lieux.replace('[', '')
                lieux = lieux.replace(']', '')
            try:
                r = requests.get(
                    "https://geo.api.gouv.fr/communes?nom=" + lieux + "&fields=centre&format=json&geometry=centre")
                ret = r.json()
            except Exception as e:
                print(e)
            if ret:
                date = row[7].replace('/', '_')
                if date[:1].isdigit() is False:
                    print('\033[93m Warning False date \033[0m')
                    continue
                my_row = {
                    "id": date + "-" + lieux,
                    "date": date,
                    "year": date[-4:],
                    "lieu": lieux,
                    "longitude": ret[0]['centre']['coordinates'][0],
                    "latitude": ret[0]['centre']['coordinates'][1],
                    "typologie": remove_accents(row[6]),
                    "path": row[10],
                    "auteur": "Rocard"
                }
                if not my_row['date'] or not my_row['lieu'] or not my_row['latitude'] or not my_row['longitude'] or not \
                my_row['path']:
                    print('\033[93m Warning Empty data \033[0m')
                    continue
                data.append(my_row)
        print(i)
        i += 1
    print(data)
    save_new_json('Discours.json', data)


def create_json_photo():
    data = []
    with open(PATH_PHOTO, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        try:
            i = 0
            for row in spamreader:
                if (i):
                    date = row[4].split(' ')
                    jour = parse_premier(str(date[0]))
                    date = jour + "_" + str(change_month(date[1])) + "_" + str(date[2])
                    my_row = {
                        "id": date + "-" + "Rocard",
                        "date": date,
                        "year": date[-4:],
                        "path": replace_recards_to_recards(row[8]),
                        "auteur": "Rocard"
                    }
                    if not my_row['date'] or not my_row['path']:
                        print('\033[93m Warning Empty data \033[0m')
                        continue
                    data.append(my_row)
                else:
                    i = 1
        except Exception as e:
            print(e)
    save_new_json('Photo.json', data)


def change_month(month):
    if (month == "janvier" or month == "jnavier"):
        return "01"
    elif (month == "février"):
        return "02"
    elif (month == "mars"):
        return "03"
    elif (month == "avril"):
        return "04"
    elif (month == "mai" or month == "ami"):
        return "05"
    elif (month == "juin" or month == "jun"):
        return "06"
    elif (month == "juillet"):
        return "07"
    elif (month == "août"):
        return "08"
    elif (month == "septembre"):
        return "09"
    elif (month == "octobre"):
        return "10"
    elif (month == "novembre" or month == "novmebre"):
        return "11"
    elif (month == "décembre"):
        return "12"
    return month


def main():
    create_json_discours()
    create_json_photo()


main()
