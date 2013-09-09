#-*- coding: utf-8 -*-
import yaml
import numpy as np
import csv

def unicode_csv_reader(utf8_data, **kwargs):
    csv_reader = csv.reader(utf8_data, delimiter = ',', **kwargs)
    for row in csv_reader:
	yield [unicode(cell, 'utf-8') for cell in row]

filename = 'spread.csv'
reader = unicode_csv_reader(open(filename))
dictype = ['Title(CC) 329', '#', 'Track list (recordings)', 'Artist', 'Label', 'Catalog number', 'Recording date', 'Barcode', 'Work', 'School', 'Role type', 'Shengqiang', 'Banshi']
infodict = {}
counter = 0
for i in reader:
	if i[0] == '':
		continue
	if counter == 0:
		counter = counter + 1
	else:
		if counter%2 == 1:
			data={}
			i = [x.split('\n')[0] for x in i]
			title = i[2]
			if title[0] == ' ':
				title = title[1:]
			for k in range(12):
				if k!=2:
					data.update({dictype[k]:i[k]})
			infodict.update({title:data})
		counter = counter + 1
#print infodict
metadata = yaml.load(file('trackInfo.yaml'))

for items in infodict.items():
	for meta in metadata:
		if items[0] == meta[1]['title']:
			meta[1].update(items[1])
