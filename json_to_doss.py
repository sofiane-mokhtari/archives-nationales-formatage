import csv, json

def open_both_json():
	with open('Photo.json', 'r', encoding='utf8') as outfile:
		with open('Discours.json', 'r', encoding='utf8') as outphoto:
			discours = json.load(outfile)
			photo = json.load(outphoto)
			print (discours)
			print (photo)

def open_json(name):
	with open(name) as f:
		data = []
		for line in f:
			data.append(json.loads(line))
	return (data)


def save_new_json(name, value):
	with open(name, 'w', encoding='utf8') as outfile:
		json.dump(value, outfile)

def main():
	data1 = open_json('Photo.json')
	data2 = open_json('Discours.json')
	print (data1)
	print (data2)

main()