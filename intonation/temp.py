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
from keyEstimation import keyFreq

try:
    filename = sys.argv[1]
except:
    print "usage:", sys.argv[0], "<input-audiofile>"
    sys.exit()

hopSize = 128
frameSize = 2048
sampleRate = 44100
guessUnvoiced = False

# RUNNING A CHAIN OF ALGORITHMS

# create our algorithms:
#run_windowing = Windowing(type='hann', zeroPadding=3*frameSize) # Hann window with x4 zero padding
#run_spectrum = Spectrum(size=frameSize * 4)
#run_spectral_peaks = SpectralPeaks(minFrequency=250, 
#                                   maxFrequency=600, 
#                                   maxPeaks=50, 
#                                   sampleRate=sampleRate,
#                                   magnitudeThreshold=0, 
#                                   orderBy="magnitude") 
#run_pitch_salience_function = PitchSalienceFunction()
#run_pitch_salience_function_peaks = PitchSalienceFunctionPeaks()
#run_pitch_contours = PitchSalienceFunctionContours(hopSize=hopSize)
#run_pitch_contours_melody = PitchSalienceFunctionMelody(guessUnvoiced=guessUnvoiced, 
#                                                hopSize=hopSize)

pool = Pool();
pitchPolyphonic = PredominantMelody(binResolution=1, guessUnvoiced=guessUnvoiced, hopSize=hopSize, minFrequency=100, maxFrequency = 1200, voicingTolerance = 1.4)
# load audio
audio = MonoLoader(filename = filename)()
[pitch, confidence] = pitchPolyphonic(audio)

# per-frame processing: computing peaks of the salience function
#for frame in FrameGenerator(audio, frameSize=frameSize, hopSize=hopSize):
#    frame = run_windowing(frame)
#    spectrum = run_spectrum(frame)  
#    peak_frequencies, peak_magnitudes = run_spectral_peaks(spectrum)
#    salience = run_pitch_salience_function(peak_frequencies, peak_magnitudes)
#    salience_peaks_bins, salience_peaks_saliences = run_pitch_salience_function_peaks(salience)
#
#    pool.add('allframes_salience_peaks_bins', salience_peaks_bins)
#    pool.add('allframes_salience_peaks_saliences', salience_peaks_saliences)
#    
## post-processing: contour tracking and melody detection
#contours_bins, contours_saliences, contours_start_times, duration = run_pitch_contours(
#        pool['allframes_salience_peaks_bins'],
#        pool['allframes_salience_peaks_saliences'])
#pitch, confidence = run_pitch_contours_melody(contours_bins, 
#                                              contours_saliences, 
#                                              contours_start_times, 
#                                              duration)
#

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

con_pitch = pitch[con_pos]
#m,b,p = hist(con_pitch, bins=int(max(con_pitch)-min(con_pitch)))


keyFreq = keyFreq(con_pitch)

# visualize output pitch
fig = plt.figure()
#value_freq = array([float(item) for item in range(n_frames)])
#tonic = 55
cents = 1200*log2(con_pitch/keyFreq)
plot(cents, 'b')
n_ticks = 10
xtick_locs = [i * (n_frames / 10.0) for i in range(n_ticks)]
xtick_lbls = [i * (n_frames / 10.0) * hopSize / sampleRate for i in range(n_ticks)]
xtick_lbls = ["%.2f" % round(x,2) for x in xtick_lbls]
plt.xticks(xtick_locs, xtick_lbls)
ax = fig.add_subplot(111)
ax.set_xlabel('Time (s)')
ax.set_ylabel('Pitch (Hz)')
suptitle("Predominant melody pitch")

plt.figure()
#m,b,p = hist(cents, bins=int(max(cents)-min(cents)))
[n, b] = histogram(cents, int(max(cents)-min(cents)))
ns = gaussian_filter(n, 10)
bc = (b[:-1]+b[1:])/2.0
ph = subplot(111)
plot(bc,ns)
ph.xaxis.set_major_locator(MultipleLocator(500))
ph.xaxis.set_major_formatter(FormatStrFormatter('%d'))
ph.xaxis.set_minor_locator(MultipleLocator(100))

ph.yaxis.set_major_locator(MultipleLocator(20))
ph.yaxis.set_minor_locator(MultipleLocator(10))

ph.xaxis.grid(True,'minor')
ph.yaxis.grid(True,'minor')
ph.xaxis.grid(True,'major',linewidth=2)
ph.yaxis.grid(True,'major',linewidth=2)

plt.figure()
plot(con_pitch)
# visualize output pitch confidence
#fig = plt.figure()
#plot(range(n_frames), confidence, 'b')
#n_ticks = 10
#xtick_locs = [i * (n_frames / 10.0) for i in range(n_ticks)]
#xtick_lbls = [i * (n_frames / 10.0) * hopSize / sampleRate for i in range(n_ticks)]
#xtick_lbls = ["%.2f" % round(x,2) for x in xtick_lbls]
#plt.xticks(xtick_locs, xtick_lbls)
#ax = fig.add_subplot(111)
#ax.set_xlabel('Time (s)')
#ax.set_ylabel('Confidence')
#suptitle("Predominant melody pitch confidence")

show()
