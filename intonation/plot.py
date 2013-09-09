#-*- coding: utf-8 -*-
from scipy.ndimage.filters import gaussian_filter
from pylab import *
import sys
from os import listdir
from os.path import isdir

if isdir(sys.argv[1]):
	mode = 'multi'
else:
	mode = 'single'
print mode

def plotFolder(dataDir, figureDir):

	datas = listdir(dataDir)
	for data in datas:
		print 'plotting ' + data
		hist = np.loadtxt(dataDir+'/'+data, delimiter="\t")
		bc = hist[:,0]
		ns = hist[:,1]
		if max(bc)-min(bc)<10:
			continue
		plt.figure()
		ph = subplot(111)
		plot(ns,bc)
		ph.xaxis.set_major_locator(MultipleLocator(500))
		ph.xaxis.set_major_formatter(FormatStrFormatter('%d'))
		ph.xaxis.set_minor_locator(MultipleLocator(100))
		ph.xaxis.limit_range_for_scale(min(ns),max(ns))
		ph.yaxis.set_major_locator(MultipleLocator(20))
		ph.yaxis.set_minor_locator(MultipleLocator(10))
		ph.xaxis.grid(True,'minor')
		ph.yaxis.grid(True,'minor')
		savefig(figureDir + '/' + data.split('.')[0]+'.png')
		close()
		#show()
		
def plotSingle(trackname, pitchFolder, keynote):
	import mbid_name	 
	mbid = mbid_name.getMBID(trackname)
	#mbid = '791dbdde-6cc1-4561-8009-3ab405ece456'
	pinyin = mbid_name.getPinyin(trackname)
	pitch = np.loadtxt(pitchFolder + '/' + mbid + '.txt', delimiter = '\t')[:,1]
	pitch = np.array([x for x in pitch if x !=0])
	plt.figure()
	cents = 1200*log2(pitch/float(keynote))
	title = pinyin + '\nKeynote = ' + keynote
	plot_Hist(cents, 'show', title, mbid)

def plot_Hist(cents, ifShow, title, mbid):
	[n, b] = np.histogram(cents, int(max(cents)-min(cents)),density = True)
	hist(cents, int(max(cents)-min(cents)))	
	show()
	ns = gaussian_filter(n, 7)
#	temp = []
#	for x in ns:
#		if x>0:
#			x = 20*np.log10(x)
#			temp.append(x)
#		else:
#			temp.append(0)
#	ns = temp
 	bc = (b[:-1]+b[1:])/2.0
	ph = subplot(111)
	plot(bc,ns)
	plt.title(title)
	ph.xaxis.set_major_locator(MultipleLocator(500))
	ph.xaxis.set_major_formatter(FormatStrFormatter('%d'))
	ph.xaxis.set_minor_locator(MultipleLocator(100))
	ph.xaxis.limit_range_for_scale(min(ns),max(ns))
		
	#ph.yaxis.set_major_locator(MultipleLocator(10))
	#ph.yaxis.set_minor_locator(MultipleLocator(5))
	ph.xaxis.grid(True,'minor')
	ph.yaxis.grid(True,'minor')
	savefig(mbid+'.png')
	if ifShow == 'show':
		show()
	
def main():
	if mode == 'multi':
		plotFolder(sys.argv[1], sys.argv[2])
	elif mode == 'single':
		plotSingle(sys.argv[1], sys.argv[2], sys.argv[3])

if __name__ == "__main__":
	main()
