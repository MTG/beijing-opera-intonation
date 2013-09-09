from essentia.standard import YamlInput, YamlOutput
import sys
import argparse
from os import listdir

def arffFeature(arffFile):
	wantedFeats = []
	wantedIndices = {}
	f = open(arffFile,'r')
	lines = f.readlines()
	for line in lines:
		if ('@attribute' in line or '@ATTRIBUTE' in line or '@Attribute' in line) and ('@relation' not in line):
			if 'segment' in line: continue
			attribute = line.split(' ')[1]
			if '-' in attribute:
				attrisp = attribute.split('-')
				if attrisp[0] in wantedFeats:
					wantedIndices[attrisp[0]].append(int(attrisp[1])-1)
				else:
					attrisp = attribute.split('-')
					wantedFeats.append(attrisp[0])
					wantedIndices.update({attrisp[0]:[int(attrisp[1])-1]})
			else:
				wantedFeats.append(attribute)
	
	return wantedFeats, wantedIndices


#This file does an in-place selection of features. Meaning selected features
#from a file are written to the same file.

fnames = sys.argv[1:]

#non-array type values in wanted features
wantedFeats = ["harmonic_spectral_centroid.mean","harmonic_spectral_centroid.var", "pitch_confidence.mean", "pitch_confidence.skew", "spectral_flatness_db.mean", "spectral_flatness_db.var", "spectral_flux.mean", "spectral_rms.mean", "spectral_rms.skew", "spectral_rolloff.mean", "spectral_strongpeak.skew", "zero_crossing_rate.mean", "mfcc.mean", "spectral_contrast.mean", "spectral_contrast.var", "tristimulus.mean", "mfcc.cov", "spectral_contrast.cov", "spectral_valley.cov"]


#array type values in wanted features
wantedIndices = {"mfcc.mean":[3, 5, 6, 7, 8], \
				"spectral_contrast.mean": [1, 2, 3], "spectral_contrast.var": [2, 3], \
				"tristimulus.mean": [2], \
				"mfcc.cov": [16, 17, 19], \
				"spectral_contrast.cov": [8, 10, 15, 16, 22], \
				"spectral_valley.cov": [2, 9, 17, 22, 29], \
				}

#Do!

cmdParser = argparse.ArgumentParser(
									description='Filter features (selected from arff file) from *.sig file.',
									epilog="Use it after got model" )
cmdParser.add_argument('--features', help='Select arff file, it reads features from it.')
cmdParser.add_argument('--inputFolder', help='sig files', default='.')
args = cmdParser.parse_args()

arffFile = args.features
fnames = listdir(args.inputFolder)
wantedFeats, wantedIndices = arffFeature(arffFile)

for fname in fnames:
	fname = args.inputFolder+'/'+fname
	fileIn = YamlInput(filename=fname)
	pool = fileIn()
	
	for descriptor in pool.descriptorNames():
		if descriptor not in wantedFeats:
			pool.remove(descriptor)
						
	for descriptor in wantedIndices.keys():
		temp = pool[descriptor]
		shape = temp.shape
		if len(shape) > 1:
			temp = temp.reshape(shape[0]*shape[1])
		pool.remove(descriptor)
		for index in wantedIndices[descriptor]:
			pool.add(descriptor, temp[index-1])
			#In essentiaToWeka, we make index 0 as element 1. (eg: mfcc.mean1). 
			#remember the wanted features are known from weka experiment! Hence index-1 !!
	output = YamlOutput(filename=fname)
	output(pool)
	

