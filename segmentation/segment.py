# -*- coding: utf-8 -*-
"""

@author: Gopala Krishna Koduri/గోపాల కృష్ణ కోడూరి


@doc_en:
To run this, you need java. After installing java, add the java executable's
path to the system path. You also need to change basecmd variable as per your
system.
"""

from os.path import walk
from os import system
from numpy import unique
import sys
import yaml

annotationFile = "annotations.yaml"

def mode(values):
	uniq_v = unique(values)
	counts = []
	for i in uniq_v:
		counts.append(values.count(i))
	i = counts.index(max(counts))
	return uniq_v[i]

def modeFilter(prediction, l):
	"""
	Mode filter customized to be biased. It will turn vocal to violin/tani but not
	viceversa. This is intended for analyzing pitch of vocal regions, for which we
	want no false positives (violin/tani) even if that means losing out a few positives.
	"""
	newPrediction = []

	if len(prediction) < l:
		for i in prediction:
			newPrediction.append(mode(prediction))
		return newPrediction
	#else:
	newPrediction.extend(prediction)
	padding = (l-1)/2
	#print padding
	for i in xrange(padding):
		prediction.insert(0, prediction[0])
		prediction.insert(-1, prediction[-1])

	for i in xrange(padding, len(prediction)-padding):
		#if prediction[i] == "vocal":
		newPrediction[i-padding] = mode(prediction[i-padding:i+padding+1])

	prediction = prediction[padding:-1*padding]
	return newPrediction

def modeFilter2(prediction):
	new_prediction = prediction
	for i in range(len(prediction)-2):
		print prediction[i:i+3]
		compare = ['instrumental','vocal','instrumental']
		if prediction[i:i+3] == compare:
			new_prediction[i:i+3] = ['instrumental','instrumental','instrumental']
		else:
			new_prediction[i:i+3] = prediction
	return new_prediction
def segment(arffFilePath):
	tmpFile =  "tmp.out"
	cmdPrefix = 'java -classpath "/Applications/weka-3-6-9.app/Contents/Resources/Java/weka.jar" weka.classifiers.lazy,IB1 -l "/Users/HarmoniCache/Desktop/features/arff/train.model" -p 0 -T '
	#cmdPrefix = 'java -classpath "C:/Program Files/Weka-3-6/weka.jar" weka.classifiers.functions.SMO -l "SMO-10-Min.model" -p 0 -T '
	cmd = cmdPrefix+'"'+arffFilePath+'" > '+tmpFile
	#print cmd
	system(cmd)
	output = file(tmpFile).readlines()
	output = output[5:-1] #wondering why? open tmpFile and look.
	timeframe = []
	prediction = []
	for i in output:
		parts = i.split()
		timeframe.append(int(parts[0]))
		temp = parts[2].split(":")
		prediction.append(temp[1])
	#print prediction
	#prediction = modeFilter(prediction,3)
	print prediction
	#print len(timeframe), len(prediction)
	prev = prediction[0]
	start = -1
	end = -1
	if prev == "vocal": start = 0
	vocalPieces = []
	for i in xrange(1, len(timeframe)):
		if start != -1 and prediction[i] != "vocal":
			end = i-1
			vocalPieces.append({'start':start*segmentLength, 'end':end*segmentLength})
			start = -1
			end = -1
		if start == -1 and prediction[i] == "vocal":
			start = i
	if start != -1 and start != i:
		if end == -1:
			end = i-1
		vocalPieces.append({'start':start*segmentLength, 'end':end*segmentLength})
	return vocalPieces

if __name__ == '__main__':
	segmentLength = 1
	modeRange = 3
	arffFilePaths = sys.argv[1:]
	annotations = yaml.load(file(annotationFile))
	if not annotations:
		annotations = {}
	for arffFilePath in arffFilePaths:
		mbid = arffFilePath.split("/")[-1].split("_")[0]
		print mbid, "being processed ..."
		try:
			vocalPieces = segment(arffFilePath)
		except:
			continue
		#print vocalPieces
		print "---------------"		
		if mbid in annotations.keys():
			print mbid+'already in'
			if 'vocal' in annotations[mbid].keys():
				annotations[mbid].pop('vocal')
			annotations[mbid]['vocal'] = {'segments': vocalPieces, 'annotator':'Kainan\'s script'}
		else:
			annotations[mbid] = {}
			annotations[mbid]['vocal'] = {'segments': vocalPieces, 'annotator':'Kainan\'s script'}
	yaml.dump(annotations, file(annotationFile, "w"), default_flow_style=False)

