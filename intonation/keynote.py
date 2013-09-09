import numpy as np
import peakDetection as pD
import sys
from pylab import *

mbid = sys.argv[1]

hist = np.loadtxt('vocal_pitch_histogram/'+mbid+'.txt')
ns = hist[:,0]
bc = hist[:,1]

valleyThresh = max(ns)/4
start = True 
check = True
doubleCheck = False
keynote = []
errors = [[2,2,2],[1,1],[3,3],[1,3],[3,1],[1,2,1]]
check = [-15,-13,-12,-10,-8,-7,-5,-3,-1,2,4,5,7,9,11,12,14,16,17,19,21,23,24,26,28,29,31,33,35,36]
forceCheck = False

while start or check:
	peaks = pD.peaks(ns,bc,method = "slope", valleyThresh = valleyThresh)['peaks']
	peaks = zip(*peaks)
	peaks.sort(key = lambda x:x[0])
	peaks = zip(*peaks)


	dist1 = []
	dist2 = []
	for i in range(0,len(peaks[0])-1):
		dist1.append(peaks[0][i+1]/100-peaks[0][i]/100)
		dist2.append(round(peaks[0][i+1])/100-round(peaks[0][i]/100))
	dist1 = [round(x) for x in dist1]
	dist2 = [round(x) for x in dist2]
	error1 = 0
	error2 = 0
	for error in errors:
		for i in range(len(dist1)):
			if dist1[i:i+len(error)] == error:
				error1 = error1 + 1
			if dist2[i:i+len(error)] == error:
				error2 = error2 + 1
	if error1 <= error2:
		dist = dist1

	else:
		dist = dist2
	error = min(error1,error2)
	if error == 0 or forceCheck == True:
		correctDist = dist
		correctPeaks = peaks
	if error > 0 and forceCheck == False:
		dist = correctDist
		peaks = correctPeaks


	if (error < 1) or forceCheck:
		keynotePos = []
		for i in range(0,len(dist)):
			value = 0
			ori = i
			if dist[i] == 1:
				while (i>=1 and value<=4):
					i = i-1
					value = value + dist[i]
					if value == 4:
						if peaks[1][ori]>peaks[1][ori+1]:
							keynotePos.append(i)
							if peaks[1][ori]<2*peaks[1][ori+1]:
								keynotePos.append(ori+1)
								doubleCheck = True
								print "Find ambiguous!"
						else:
							keynotePos.append(ori+1)

			elif dist[i] == 3:
				while (i>=1 and value<=2):
					i = i-1
					value = value + dist[i]
					if value == 4:
						keynotePos.append(i)

		keynotes = [peaks[0][x] for x in keynotePos]
		if keynotes == []:
			valleyThresh = valleyThresh/2
		else:
			start = False
	
	print "Checking redundant ..."
	while len(keynotes) > 1:
		for i in range(1,len(keynotes)):
			distance = []
			for j in range(i):
				distance.append(keynotes[i]-keynotes[j])
			for k in distance:
				if (1100<k and k<1300) or k < 50:
					keynotes[i] = -10000
		try:
			keynotes.remove(-10000)
		except:
			break

	if len(keynotes) > 1 or doubleCheck == True:
		print "Double checking ..."
		correction = []
		for key in keynotes:
			keyPos = [i for i,x in enumerate(peaks[0]) if x == key]
			keyPos = keyPos[0]
			match = 0
			negative = 0
			positive = 0
			for i in range(len(dist)):
				if i<=keyPos and i>0:
					negative = negative - dist[keyPos-i] 
					try:
						check.index(negative)
						match = match + peaks[1][i] 
					except:
						continue
				else:
					if i == 0: 
						positive = positive + dist[keyPos]
					else:
						positive = positive + dist[i]	
					try:
						check.index(positive)
						match = match + peaks[1][i+1]
					except:
						continue
			correction.append(match)
			print "frequency " + str(key) + ' has match: ' + str(match)

	if len(keynotes)!=0:
		forceCheck = False

	
	if keynote == keynotes or error>0:
		if len(keynotes) == 1:
			keynote = keynotes
			check = False
		elif len(keynotes) == 0:
			print "No keynote is found, force to down valley check..."
			forceCheck = True
		else:
			for i in range(len(keynotes)):
				if (keynotes[i]<3950 and  keynotes[i]>3650) or (keynotes[i]<2550):
					keynotes[i] = -10000
					correction[i] = -10000
			try:
				keynotes.remove(-10000)
				correction.remove(-10000)
			except:
				pass
			keynote = [keynotes[i] for i,x in enumerate(correction) if x==max(correction)]
			check = False
	else:
		print dist
		print error
		print keynotes
		print keynote
		print "Down valley threshold checking ................"
		valleyThresh = valleyThresh/2
		keynote = keynotes

print "Number of errors left: " + str(error)
print keynote

keyPos = [peaks[0][i] for i,x in enumerate(peaks[0]) if x==keynote]
notePos = np.zeros(len(peaks[0]))

notePos[0] = round(peaks[0][0]-keynote) + peaks[0][0] - peaks[0][1] - round(peaks[0][0] - peaks[0][1])
notePos[-1] = round(peaks[0][-1]-keynote) + peaks[0][-1] - peaks[0][-2] - round(peaks[0][-1] - peaks[0][-2])
for i in range(1,len(peaks[0])-1):
	if peaks[0][i] != keynote: 
		offset = (peaks[0][i+1] - peaks[0][i] - round(peaks[0][i+1] - peaks[0][i])) + (peaks[0][i] - peaks[0][i-1] - round(peaks[0][i] - peaks[0][i-1]))
	else:
		offset = 0
	notePos[i] = round(peaks[0][i]-keynote) + offset

ph = subplot(111)
stem(notePos,peaks[1])
ph.xaxis.set_major_locator(MultipleLocator(500))
ph.xaxis.set_major_formatter(FormatStrFormatter('%d'))
ph.xaxis.set_minor_locator(MultipleLocator(100))
ph.xaxis.limit_range_for_scale(min(ns),max(ns))
ph.yaxis.set_major_locator(MultipleLocator(20))
ph.yaxis.set_minor_locator(MultipleLocator(10))
ph.xaxis.grid(True,'minor')
ph.yaxis.grid(True,'minor')
grid(True,which='both',axis='x')
print notePos, peaks[1]
show()
