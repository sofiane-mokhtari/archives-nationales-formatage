import csv, json
import unicodedata
import requests

def save_new_json(name, value):
	with open(name, 'w', encoding='utf8') as outfile:
		json.dump(value, outfile)

def remove_accents(input_str):
	nfkd_form = unicodedata.normalize('NFKD', input_str)
	return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

def create_json_discours() :
	data = []
	with open('03_le_politique_parle_au_citoyen\Rocard - Allocutions - Inventaire\FRAN_IR_050330_Rocard_allocutions.csv', newline='') as csvfile:
		try :
			spamreader  = csv.reader(csvfile, delimiter=';')
		except Exception as e:
			print (e)
		try:
			for row in spamreader:
					lieux = remove_accents((row[5].split(","))[0])
					if (lieux != "S. l."):
						departement = lieux.split('(')
						if (len(departement) == 2) :
							lieux = departement[0][:-1]
						try :
							r = requests.get("https://geo.api.gouv.fr/communes?nom="+lieux+"&fields=centre&format=json&geometry=centre")
						except Exception as e:
							print (e)
						ret = r.json()
						if ret :
							my_row ={
								"id": row[7] + "-" + lieux,
								"date": row[7],
								"lieu": lieux,
								"longitude": ret[0]['centre']['coordinates'][0],
								"latitude": ret[0]['centre']['coordinates'][1],
								"typologie": remove_accents(row[6]),
								"path": row[10],
								"auteur": "Rocard" 
								}
							data.append(my_row)
			save_new_json(Discours.json, data)
		except Exception as e:
			print (e)

def create_json_photo() :
	with open('Photo.json', 'w', encoding='utf8') as outfile:
		with open('03_le_politique_parle_au_citoyen\Rocard - Reportages photographiques - Inventaire\\rocard_FRAN_IR_050535_photos.csv', newline='') as csvfile:
			spamreader  = csv.reader(csvfile, delimiter=';')
			try:
				i = 0
				for row in spamreader:
					if (i) :
						date = row[4].split(' ')
						date = str(date[0]) + "-" + str(change_month(date[1])) + "-" + str(date[2])
						my_row ={
							"id": date + "-" + "Rocard",
							"date": date,
							"path": row[8],
							"auteur": "Rocard" 
							}
						out = json.dumps(my_row, indent=4, sort_keys=True, separators=(',', ': '), ensure_ascii=False)
						outfile.write(out)
						outfile.write("\n")
					else :
						i = 1
			except Exception as e:
				print (e)

def change_month(month):
	if (month == "janvier"):
		return 1
	elif (month == "février"):
		return 2
	elif (month == "mars"):
		return 3
	elif (month == "avril"):
		return 4
	elif (month == "mai"):
		return 5
	elif (month == "juin"):
		return 6
	elif (month == "juillet"):
		return 7
	elif (month == "aout"):
		return 8
	elif (month == "septembre"):
		return 9
	elif (month == "octobre"):
		return 10
	elif (month == "novembre"):
		return 11
	elif (month == "decembre"):
		return 12


def main():
	create_json_discours()
	create_json_photo()

main()