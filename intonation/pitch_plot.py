import sys, csv
from essentia import *
from essentia.standard import *
from pylab import *
from numpy import *
from math import log
from math import floor
import matplotlib.pyplot as pyplot
from scipy.ndimage.filters import gaussian_filter
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

def wav_pitch(filename):

	hopSize = 128
	frameSize = 2048
	sampleRate = 44100
	guessUnvoiced = False

	# RUNNING A CHAIN OF ALGORITHMS
	pool = Pool();
	pitchPolyphonic = PredominantMelody(binResolution=1, guessUnvoiced=guessUnvoiced, hopSize=hopSize, minFrequency=100, maxFrequency = 1200, voicingTolerance = 1.2)
	# load audio
	audio = MonoLoader(filename = filename)()
	[pitch, confidence] = pitchPolyphonic(audio)
	con_pos = [i for i,x in enumerate(confidence) if x > 0]
	n_frames = len(con_pos)
	print "number of frames:", n_frames

	fig = plt.figure()
	plot(pitch, 'b')
	n_ticks = 10
	xtick_locs = [i * (n_frames / 10.0) for i in range(n_ticks)]
	xtick_lbls = [i * (n_frames / 10.0) * hopSize / sampleRate for i in range(n_ticks)]
	xtick_lbls = ["%.2f" % round(x,2) for x in xtick_lbls]
	plt.xticks(xtick_locs, xtick_lbls)
	ax = fig.add_subplot(111)
	ax.set_xlabel('Time (s)')
	ax.set_ylabel('Pitch (Hz)')
	suptitle("Predominant melody pitch")

	return pitch
