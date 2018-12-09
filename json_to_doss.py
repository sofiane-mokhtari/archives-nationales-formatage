from shutil import copyfile
import csv, json, os, time

PATH_TO_DATASET = "/Users/victorguerand/Desktop/03 - Le politique parle au citoyen/Rocard - reportages photographiques"

PATH = "/Users/victorguerand/test_Archive/formatage_donnee"


def read_json(name):
    with open(name) as f:
        data = json.load(f)
    return (data)

def save_new_json(name, value):
    with open(name, 'w', encoding='utf8') as outfile:
        json.dump(value, outfile)

def replace_recards_to_recards(path):
	return path.replace("Rocards", "Rocard")


def get_element_json(name, element):
    data = read_json(name)
    return (data[0][element])


def get_element_json(name, element, t_value):
    ret = []
    data = read_json(name)
    for line in data:
        if (time.strptime(line[element], "%d_%m_%Y") == time.strptime(t_value, "%d_%m_%Y")):
            ret.append(line)
    return (ret)


def move_dir(path, name):
    path = replace_recards_to_recards(path)
    if (os.path.exists(path)):
        copyfile(path, name + '.jpeg')
        print('\033[92m  Done {}  \033[0m'.format(name))
    else:
        print("fdp")


def add_value_json(name, element, value):
    data = read_json(name)
    for row, val in data, value:
        row[element] = value
    save_new_json(name, data)

def normalize_path(path):
    path_input = path.replace('\\', '/')
    return path_input


def main():
    dis = "Discours.json"
    photo = "Photo.json"
    data = read_json(dis)
    for line in data:
        path = line['auteur'] + "\\" + line['date'] + "-" + line['lieu'] + "\\" + "Images"
        ret = get_element_json(photo, 'date', line['date'])
        if ret:
            path = normalize_path(path)
            path = PATH + '/' + path
            print(path)
            if (os.path.isdir(path)):
                i = 0
                for file in ret:
                    move_dir(normalize_path(PATH_TO_DATASET + file['path'][2:]), path + '/' + line['date'] + "-" + line['lieu'] + "-" + str(i),)
                    i += 1
            else:
                print("yes")


main()
