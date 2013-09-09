from pylab import *
import sys
#import pitch_hist
import numpy as np
import yaml
import pdb
from os.path import exists


pitchDir = sys.argv[1]
pitchFiles = sys.argv[2]
def FindNearestIndex(arr,value):
#For a given value, the function finds the nearest value in the array and returns its index.
	#pitch = pitch_hist.wav_pitch(filename)
	#pitch = pitch_hist.wav_pitch(filename)
	arr = np.array(arr)
	index=(np.abs(arr-value)).argmin()
	return index


segmentation = yaml.load(file("annotations.yaml"))

for track in segmentation.keys():
	vocal_pitch = []
	seg = segmentation[track]['vocal']['segments']
	filename = str(pitchFiles) + '/' + str(track)+'.txt'
	if exists(pitchDir+"/"+track+".txt"): continue
	print filename
	pitch = np.loadtxt(filename, delimiter="\t")
	vocal_pitch = np.zeros(np.shape(pitch))
	for vocal in seg:
		start = FindNearestIndex(pitch[:,0],vocal['start'])
		end = FindNearestIndex(pitch[:,0],vocal['end']+1)
		vocal_pitch[start:end] = pitch[start:end]
	for i in range(len(vocal_pitch)):
		if vocal_pitch[i][2]<=0:
			vocal_pitch[i][1] = 0
	np.savetxt(pitchDir+"/"+track+".txt", vocal_pitch, delimiter="\t")	
