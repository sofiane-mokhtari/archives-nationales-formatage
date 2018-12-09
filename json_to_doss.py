import csv, json, os, time

def read_json(name):
	with open(name) as f:
		data = json.load(f)
	return (data)

def save_new_json(name, value):
	with open(name, 'w', encoding='utf8') as outfile:
		json.dump(value, outfile)

def get_element_json(name, element):
	data = read_json(name)
	return (data[0][element])

def get_element_json(name, element, t_value):
	ret = {}
	print (t_value)
	data = read_json(name)
	for line in data:
		if (time.strptime(line[element], "%d_%m_%Y") == time.strptime(t_value, "%d_%m_%Y")):
			ret[0].append(line)
	return (ret)

def move_dir(path, name):
	if (os.path.isdir(path)):
		os.rename(path, name)

def add_value_json(name, element, value):
	data = read_json(name)
	for row,val in data, value:
		row[0][element] = value
	save_new_json(name, data)

def main():
	dis = "Discours.json"
	photo = "Photo.json"
	data = read_json(dis)
	path = os.path.isdir(line[0]['auteur'])
	path2 = path + "\\" + os.path.isdir(line[0]['date']) + "-" + os.path.isdir(line[0]['lieux'])
	for line in data:
		ret = get_element_json(photo, 'date', line['date'])
		if (os.path.isdir(path)):
			if (os.path.isdir(path2):
				if (os.path.isdir(path2 + "\\" + "Images"):
					for file in ret :
						move_dir(file['path'], path2 + "\\" + "Images")

main()