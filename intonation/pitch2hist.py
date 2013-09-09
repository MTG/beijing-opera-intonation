from scipy.ndimage.filters import gaussian_filter
from os import listdir
import numpy as np
import sys
from pylab import *

histDir = sys.argv[1]
pitchFilesDir = sys.argv[2]

pitchFiles = listdir(pitchFilesDir)
tracks = [x.split('.')[0] for x in pitchFiles if x[-3:]=='txt']
for pitchFile in pitchFiles:
	print 'start working on ' + pitchFile
	pitch = np.loadtxt(pitchFilesDir+'/'+pitchFile, delimiter="\t")[:,1]
	pitch = np.array([x for x in pitch if x!=0])
	cents = 1200*np.log2(pitch/55)
	[n, b] = np.histogram(cents, int(max(cents)-min(cents)),density = True)
	ns = gaussian_filter(n, 7)
	bc = (b[:-1]+b[1:])/2.0
	pitchistogram = np.zeros([len(ns),2])
	pitchistogram[:,0] = ns
	pitchistogram[:,1] = bc
	np.savetxt(histDir+"/"+pitchFile.split('.')[0]+".txt", pitchistogram, delimiter="\t") 
