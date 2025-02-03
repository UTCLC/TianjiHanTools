import csv
import configparser

config = configparser.ConfigParser()

global lang
global langs
global keys
lang = "en"
langs = []
keys = {}
with open("loc.csv",encoding="utf-8") as f:
	reader = csv.reader(f)
	for line in reader:
		if (line):
			if (line[0] == "keys"):
				for langi in line:
					if (langi != "keys"):
						langs.append(langi)
						keys[langi] = {}
			else:
				for stri in line:
					if (line.index(stri) != 0):
						keys[langs[line.index(stri)-1]][line[0]] = stri
# print(keys)
config.read("config.ini")
lang = config.get("generic","lang",fallback="en")

def translate(key):
	if (key in keys[lang]):
		return keys[lang][key]
	elif (key in keys["en"]):
		return keys["en"][key]
	else:
		print("Error: Undefined key: "+key)
		return key