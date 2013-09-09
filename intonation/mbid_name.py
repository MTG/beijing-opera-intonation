#coding=utf-8 
import sys
import yaml
import numpy as np

#infoDir = sys.argv[1]
infoDir = 'trackInfo.yaml'
trackName = sys.argv[1]

def getmapping(infoDir):
	items = yaml.load(file(infoDir))
	mapping = []
	#mapping = np.array(('mbid','name'), dtpye = dtype)
	for item in items.items():    
		title = item[1]['title']
		pinyin = item[1]['title(pinyin)']
		value = [item[0], title, pinyin]
		mapping.append(value)
	return mapping

def getMBID(trackname):
	infoDir = 'trackInfo.yaml'
	trackname = trackname.decode('utf-8')
	mapping = getmapping(infoDir)
	names = [x[1] for x in mapping]
	pos = names.index(trackname)
	return mapping[pos][0]

def getPinyin(trackname):
	infoDir = 'trackInfo.yaml'
	trackname = trackname.decode('utf-8')
	mapping = getmapping(infoDir)
	names = [x[1] for x in mapping]
	pos = names.index(trackname)
	return mapping[pos][2]
MBID = getMBID(trackName)
print MBID

