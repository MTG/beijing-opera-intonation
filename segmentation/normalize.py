# -*- coding: utf-8 -*-

#This is to be run after essentiaToWeka.py
#Handling nans and infs:
#infs: negative inf is set to min of the range of feature values and viceversa
#nans: set to 0

import sys
import numpy as np
from os import unlink
from os.path import basename

topLimit=100000

#arguments:
if len(sys.argv) < 2:
	print """
	Usage:
	------
	python normalize.py 'train' trainFile normalizedTrainFile (OR)
	python normalize.py 'test' trainFile testFiles destDirectory
	"""
	exit()

#[train] [trainFile] [normalizedTrainFile]
#[test] [trainFile] [testFile] [normalizedTestFile]

if sys.argv[1] == "train":
	#look all the values for each feature and find max and min, and normalize to (0-1)
	temp = file(sys.argv[2], "r").readlines()
	prologue = ""
	for line in temp:
		prologue += line
		if line.strip() == "@DATA":
			break
	numFeats = len(temp[-1].strip().split(","))-1
	del temp
	data = np.loadtxt(sys.argv[2], dtype='float', delimiter=',', comments='@', usecols=range(numFeats))
	for i in xrange(numFeats):
		temp = data[:, i]
		infAlert = 0
		if max(temp) == np.inf:
			infAlert = 1
			temp = temp[temp < np.inf]
		if min(temp) == -np.inf:
			infAlert = 1
			temp = temp[temp > -np.inf]
		_max = max(temp)
		_min = min(temp)
		data[:, i] = (data[:, i]-_min)/(_max-_min)
		#TODO: Is there a better way to handle inf & nan values?
		_min = min(abs(data[:, i])) 
		#The following is because weka complains if the numbers are too small (I guess 1.0e-8)
		if infAlert:
			data[:, i][data[:, i] == np.inf] = topLimit
			data[:, i][data[:, i] == -np.inf] = 0
		data[:, i] = np.nan_to_num(data[:, i])
		data[:, i] = data[:, i]*topLimit
#	for i in xrange(numFeats):
#		print i, max(data[:, i]), min(data[:, i])
	outfile = file(sys.argv[3], 'w')
	outfile.write(prologue)
	labels = np.loadtxt(sys.argv[2], dtype='float', comments='@', delimiter=',', usecols=[numFeats])
	float_labels = []
	'''
	for label in labels:
		if label == 'instrumental':
			float_labels.append(1.)
		else:
			float_labels.append(0.)
	'''
	data = np.column_stack([data, labels])
	np.savetxt('dataTMP.txt', data, delimiter=',')
	#Weird. Python does not seem to have a nice way to 'append' array data to a file. 
	#It can only create a new file and write.
	temp = file('dataTMP.txt', 'r').read()
	unlink('dataTMP.txt')
	outfile.write(temp)
	outfile.close()

elif sys.argv[1] == "test":
	#read limits obtained from train data and do normalization accordingly
	#temp = file(sys.argv[2], "r").readlines()
	#numFeats = len(temp[-1].strip().split(","))-1
	#del temp
	numFeats = 36 #NOTE: Hardcoded to reduce i/o, uncomment the above lines and delete this if necessary
	data = np.loadtxt(sys.argv[2], dtype='float', delimiter=',', comments='@', usecols=range(numFeats))
	trainLimits = []
	for i in xrange(numFeats):
		temp = data[:, i]
		infAlert = 0
		temp = temp[temp < np.inf]
		temp = temp[temp > -np.inf]
		_max = max(temp)
		_min = min(temp)
		trainLimits.append([_min, _max])

	#prologue is same for every file. read for one, and write for all.
	temp = file(sys.argv[3], "r").readlines()
	prologue = ""
	for line in temp:
		prologue += line
		if line.strip() == "@DATA":
			break
	#numFeats = len(temp[-1].strip().split(","))-1
	del temp
	for f in sys.argv[3:-2]:
		print f
		data = np.loadtxt(f, dtype='float', delimiter=',', comments='@', usecols=range(numFeats))
		for i in xrange(numFeats):
			temp = data[:, i]
			_min = trainLimits[i][0]
			_max = trainLimits[i][1]
			data[:, i] = (data[:, i]-_min)/(_max-_min)
			#TODO: Is there a better way to handle inf & nan values?
			_min = min(abs(data[:, i])) 
			data[:, i][data[:, i] == np.inf] = topLimit
			data[:, i][data[:, i] == -np.inf] = 0
			data[:, i] = np.nan_to_num(data[:, i])
			#The following is because weka complains if the numbers are too small (I guess 1.0e-8)
			data[:, i] = data[:, i]*topLimit
		
		outfile = file(sys.argv[-1]+"/"+basename(f), 'w')
		outfile.write(prologue)
		np.savetxt('dataTMP.txt', data, delimiter=',')
		#Weird. Python does not seem to have a nice way to 'append' array data to a file. 
		#It can only create a new file and write.
		temp = file('dataTMP.txt', 'r').readlines()
		unlink('dataTMP.txt')
		for line in temp:
			line = line.strip()
			line = line+",?\n"
			outfile.write(line)
		outfile.close()
