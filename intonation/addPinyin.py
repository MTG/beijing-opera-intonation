#-*- coding: utf-8 -*-
import pinyin
import yaml

data = yaml.load(file('trackInfo.yaml'))

tracks = data.items()

for track in tracks:
	#title = track[1]['title']
	try:
		
		artist = track[1]['School']
		#role = track[1]['Role type']
		piny = ''
		for char in artist:
			if char == u'：':
				pinyi = ': '
			elif char == u'、':
				pinyi = '. '
			elif char == u'·':
				pingi = '. '
			elif char == u'—':
				pinyi = '- '
			elif char == u'《':
				pinyi = '<'
			elif char == u'》':
				pinyi = '> '
			elif char == u'【':
				pinyi = '['
			elif char == u'】':
				pinyi = '] '
			elif char == u'“':
				pinyi = '\"'
			elif char == u'”':
				pinyi = '\" '
			elif char == u'‘':
				pinyi = '\''
			elif char == u'’':
				pinyi = '\' '
			elif char == u'（':
				pinyi = '('
			elif char == u'）':
				pinyi = ') '
			else:
				pinyi = pinyin.get(char) + ' '
			piny = piny + pinyi
		if piny[-1]==' ':
			piny = piny[:-1]
		track[1].update({'School(pinyin)':piny})
	except:
		continue	
yaml.dump(data, file('trackInfo.yaml', "w"), default_flow_style=False)
