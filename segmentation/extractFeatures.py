# -*- coding: utf-8 -*-
"""
@author: Kainan Chen
	
@doc_en:
This script extracts features using essentia, and store them in the yaml format but with .sig at the end of filenames.
It can compute for a single audio or folder with multi-audio by the segment step by step with the specified length or the whole audio(default) and hopsize.

@example:
	Multi-audio compute:
		python extractFeatures.py --inputFolder FOLDERWITHAUDIO --outputFolder FOLDEROUT --length SEGMENTLENGTH --hopsize HOPSIZE
	Single-audio compute:
		python extractFeatures.py --inputFile FOLDERWITHAUDIO --outputFolder FOLDEROUT --length SEGMENTLENGTH --hopsize HOPSIZE

	inputFolder (default '.')
	outputFolder (default '.')
	inputFile (No sensitive default)
	length (default 1 sec)
	hopsize (default 0, no overlap)
	
@note:
	This script uses lib Essentia, developed by MTG@UPF, Spain with the version of 2.0.
"""


from os.path import exists, walk, isdir #is different from os.walk!
from essentia import Pool
from os import mkdir
import essentia.standard as es
import sys
import wave
from numpy import log10, square, sqrt, arange
import argparse

def extractFeatures(arffDir = '.', dirname = '.', fnames = '', segment_length = 'WHOLE', hopsize = 0):
	# Start to process file by file from input
	for fname in fnames:
		# It only process wav or mp3 file
		if ".wav" not in fname.lower() and ".mp3" not in fname.lower(): continue

		# Generate output dir
		trackName = fname.split('/')[-1]
		segmentArffDir = arffDir+"/"+trackName[:-4]+"/"
		if not exists(segmentArffDir):
			mkdir(segmentArffDir)
		else:
			print fname + ' exsits, pass...'
			continue
		
		# Read audio and some more info
		loader = es.EasyLoader(filename = dirname+"/"+fname)
		audio = loader.compute()
		sampleRate = loader.paramValue('sampleRate')
		length = int(len(audio)/sampleRate)
		if length == 0: length = 1
		print fname + ' length: ' + str(length) 

		if hopsize == 0:
			hopsize = segment_length
			
		# Specify the length of the segment
		if segment_length == 'WHOLE':
			step = length
			end_time = length
			segment_length = length
			print 'The whole audio is being processed...'
		else:
			step = hopsize
			segment_length = float(segment_length)
			if step>length: continue

		# Start computing segment by segment
		for start_time in arange(0, length, step):
			end_time = start_time + segment_length
			if step != length:
				print 'the time from second ' + str(start_time) + ' is being processed...'
			if end_time > length:
				break;
			segAudio = audio[start_time*sampleRate:end_time*sampleRate]
			pool = Pool()

			# Setup parameters 
			specContrast = es.SpectralContrast(frameSize=2048, lowFrequencyBound=40, sampleRate=sampleRate)
			spectrum = es.Spectrum(size=2048) #size is frameSize
			mfcc = es.MFCC(lowFrequencyBound=40, sampleRate=sampleRate) # MFCC
			if step > 20:
				hpcp = es.HPCP(size = 12, referenceFrequency = 440, harmonics=8, bandPreset = True, minFrequency = 40.0, maxFrequency = 5000.0, \
					splitFrequency = 500.0, weightType = 'cosine', nonLinear = False, windowSize = 1);# HPCP
			lowLevelSpectralExtractor = \
				es.LowLevelSpectralExtractor(frameSize=2048, hopSize=1024, sampleRate=sampleRate)
			spectralPeaks = es.SpectralPeaks(sampleRate=sampleRate, minFrequency=40, maxFrequency=11000, maxPeaks=50, magnitudeThreshold=0.2)

			# Low level spectral feature analysis
			try:
				features = lowLevelSpectralExtractor(segAudio)
			except:
				print start_time, "has failed!"
				continue
			
			
			# Harmonic spectral features (TODO: Is the magnitude threshold ok?)
			harmonicPeaks = es.HarmonicPeaks()
			pitch = es.PitchDetection()	# Using YIN instead of predominant pitch analysis as this frame-based analysis


			# Windowing
			window = es.Windowing(size=2048)
			for frame in es.FrameGenerator(segAudio, frameSize=2048, hopSize=1024):
				# spectral contrast
				s = spectrum(window(frame))
				contrast, valley = specContrast(s)
				pool.add('spectral_contrast', contrast)
				pool.add('spectral_valley', valley)

				# MFCC
				bands, mfccs = mfcc(s)
				pool.add('mfcc', mfccs[1:])

				freqs, mags = spectralPeaks(s)

				# HPCP
				if step > 20:
					hpcps = hpcp(freqs, mags)
					pool.add('HPCP', hpcps) 

				# Self-compute spectral features
				if len(freqs) > 0:
					p, conf = pitch(s)
					if freqs[0] == 0:
						freqs = freqs[1:]
						mags = mags[1:]
					freqs, mags = harmonicPeaks(freqs, mags, p)
					_sum = 0
					if len(freqs) == 1:
						specEnvelope_i = [freqs[0]] #for hsd
						_sum = freqs[0]*mags[0]
					elif len(freqs) == 2:
						specEnvelope_i = [(freqs[0]+freqs[1])/2.0] #for hsd
						_sum = freqs[0]*mags[0]+freqs[1]*mags[1]
					elif len(freqs) > 2:
						specEnvelope_i = [(freqs[0]+freqs[1])/2.0] #for hsd
						_sum = freqs[0]*mags[0]
						for i in xrange(1, len(freqs)-1):
							_sum += freqs[i]*mags[i] #for hsc_i
							specEnvelope_i.append((freqs[i-1]+freqs[i]+freqs[i+1])/3.0)
						specEnvelope_i.append((freqs[i]+freqs[i+1])/2.0)
						_sum += freqs[i+1]*mags[i+1]
					hsc_i = _sum/sum(mags)
					pool.add('harmonic_spectral_centroid', hsc_i)
					hsd_i = sum(abs(log10(mags)-log10(specEnvelope_i)))/sum(log10(mags))
					pool.add('harmonic_spectral_deviation', hsd_i)
					hss_i = sqrt(sum(square(freqs-hsc_i)*square(mags))/sum(square(mags)))/hsc_i
					pool.add('harmonic_spectral_spread', hss_i)
				else:
					pool.add('harmonic_spectral_centroid', 0)
					pool.add('harmonic_spectral_deviation', 0)
					pool.add('harmonic_spectral_spread', 0)


			for i in xrange(0, len(features[0])):
			#	pool.add('barkbands', features[0][i])
				pool.add('hfc', features[4][i])
				pool.add('pitch', features[6][i])
				pool.add('pitch_instantaneous_confidence', features[7][i])
				pool.add('pitch_salience', features[8][i])
				pool.add('silence_rate_20dB', features[9][i])
			#	pool.add('silence_rate_30dB', features[10][i])
			#	pool.add('silence_rate_60dB', features[11][i])
				pool.add('spectral_complexity', features[12][i])
				pool.add('spectral_crest', features[13][i])
				pool.add('spectral_decrease', features[14][i])
				pool.add('spectral_energy', features[15][i])
			#	pool.add('spectral_energyband_low', features[16][i])
			#	pool.add('spectral_energyband_middle_low', features[17][i])
			#	pool.add('spectral_energyband_middle_high', features[18][i])
			#	pool.add('spectral_energy_high', features[19][i])
				pool.add('spectral_flatness_db', features[20][i])
				pool.add('spectral_flux', features[21][i])
				pool.add('spectral_rms', features[22][i])
				pool.add('spectral_rolloff', features[23][i])
				pool.add('spectral_strongpeak', features[24][i])
				pool.add('zero_crossing_rate', features[25][i])
				pool.add('inharmonicity',  features[26][i])
				pool.add('tristimulus',  features[27][i])
			
			onsetRate = es.OnsetRate()
			onsets, rate = onsetRate(segAudio)
			try:
				aggrPool = es.PoolAggregator(defaultStats = ['mean', 'var', 'skew', 'kurt'])(pool)
			except:
				print start_time/step, "failed"
				continue

			aggrPool.add('onset_rate', rate)
							
			#print start_time, segment_length, start_time/segment_length
			fileout = segmentArffDir+trackName[:-4]+"_%003d%s"%(start_time/step, ".sig")
			output = es.YamlOutput(filename = fileout)
			output(aggrPool)

def processDirectory(args, dirname, fnames):
	extractFeatures(arffDir = args[0], dirname = dirname, fnames = fnames ,segment_length = segment_length, hopsize = hopsize)

def main(wavDir, arffDir, segment_length, hopsize):
	"""
	main(wavDir, arffDir)
	wavDir: The complete path to the folder with set of wav files of 
	which the features are to be calculated. This folder can have several 
	levels of sub folders.
	arffDir: The complete path to the folder where the features have to be
	saved. For each wav file, a folder is created by its name in this folder.
	"""
	print 'Segment length is: ' + str(segment_length) + ' second. and the hopsize is ' + str(hopsize)
	walk(wavDir, processDirectory, (arffDir,segment_length, hopsize))

if __name__ == '__main__':
	cmdParser = argparse.ArgumentParser(
		description='Extract low-level features with specified step length and hop size.',
		epilog="Extract audio low-level features" )

	cmdParser.add_argument('--length', help='Segment length',default='WHOLE')
	cmdParser.add_argument('--hopsize', help='Hop size', default=0)
	cmdParser.add_argument('--inputFolder', help='Input folder with audio',default='.')
	cmdParser.add_argument('--outputFolder', help='Onput folder with features',default='.')
	cmdParser.add_argument('--inputFile', help='Input audio file directly', default=1)
	args = cmdParser.parse_args()
	
	segment_length =  args.length
	hopsize = float(args.hopsize)
	wavDirs = args.inputFolder
	audioFile =  args.inputFile
	arffDir = args.outputFolder
	
	if audioFile == 1:
		main(wavDirs, arffDir, segment_length, hopsize)
		print "Done!"
		
	elif wavDirs != '.':
		print "Sorry, cannot compute both single file and folder."
		exit()
	
	else:
		extractFeatures(arffDir = arffDir, fnames = [audioFile], segment_length = segment_length, hopsize = hopsize)

