# -*- coding: utf-8 -*-
"""
@author: Kainan Chen

@doc_en: From feature extracted by essentia (.sig) to Weka file (.arff) with specified label, clusters (default = [wanted, other])
	
@example:
	
	python essentiaToWeka.py --inputFolder inputFolder --label voice --clusters voice,instrument
	
"""

from os import listdir
import essentia.standard as es
import numpy as np
import sys
import argparse

def sortNumerical(s):
	return int(s[:-4])

def toWeka(pathGiven, label, clusters):
	print pathGiven
	parts = pathGiven.rstrip("/").split("/")
	parentDir = "/".join(parts[:-1])
	arffFilename = "/".join([parentDir, parts[-1]+".arff"])
	wekafile=file(arffFilename, "w+")
	relation_name = "segmentation"
	wekafile.write("@RELATION segmentation\n\n")
	all_labels = clusters.split(',')
	
	#write the descriptor details only once
	descriptor_flag = 0
	
	extension = ".sig"
	fnames = np.sort(listdir(pathGiven))
	#fnames.sort(key=sortNumerical)
	for fname in fnames:
		print fname
		if (fname.endswith(extension)):
			fname = pathGiven+"/"+fname
			yamlinput = es.YamlInput(filename=fname)
			pool = yamlinput()
			descriptorList = pool.descriptorNames()
			descriptorList.remove('metadata.version.essentia')
			
			#write descriptors details (once)
			if descriptor_flag == 0:
				attr_list = ""
				for i in descriptorList:
					if isinstance(pool[i], float):
						attr_list = attr_list + "@ATTRIBUTE "+i+" REAL\n"
					elif isinstance(pool[i], np.ndarray):
						shape = pool[i].shape
						_len = shape[0]
						if len(shape) > 1:
							_len = shape[0]*shape[1]
						for j in xrange(_len):
							attr_list = attr_list + "@ATTRIBUTE "+i+'-'+str(j+1)+" REAL\n"
				attr_list = attr_list+"\n@ATTRIBUTE segment {"+", ".join(all_labels)+"}\n\n@DATA\n"
				wekafile.write(attr_list)
				descriptor_flag = 1
			
			#write the data points
			data_entry = ""
			for i in descriptorList:
				if isinstance(pool[i], float):
					data_entry = data_entry+str(pool[i])+", "
				elif isinstance(pool[i], np.ndarray):
					data = pool[i]
					shape = data.shape
					if len(shape) > 1:
						data = data.reshape(shape[0]*shape[1])
					data_entry = data_entry+", ".join(str(x) for x in data)+", "
			data_entry = data_entry+label
			wekafile.write(data_entry+"\n")

if __name__ == '__main__':
	#For building model
	#toWeka("../data/vocal/features-selfeats", "0.000000000000000000e+00")
	#toWeka("../data/violin/features-selfeats", "1.000000000000000000e+00")
	#toWeka("../data/tani/features-selfeats", "2.000000000000000000e+00")
	#toWeka("../data/test/", "2.000000000000000000e+00")
	
	#For using the built model
	#pathGiven = sys.argv[1]
	cmdParser = argparse.ArgumentParser(
										description='You can specify the label and cluster names',
										epilog="Convert essentia data to *.arff" )
	cmdParser.add_argument('--inputFolder', help='the folder contains sig files',default='.')
	cmdParser.add_argument('--label', help='label', default='?')
	cmdParser.add_argument('--clusters', help='whole clusters names, separated by comma', default='wanted,other')
	args = cmdParser.parse_args()
	
	pathsGiven = args.inputFolder
	label = args.label
	clusters = args.clusters
	
	for pathGiven in [pathsGiven]:
		toWeka(pathGiven, label, clusters)
	print "Done!"
