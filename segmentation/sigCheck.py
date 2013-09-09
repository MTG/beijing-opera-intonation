# -*- coding: utf-8 -*-
"""
@author: Kainan Chen

@doc_en:
This script should be (necessary!) run before run 'essentiaToWeka.py' to the extracted features (*.sig), to fix the file missing and file name problems.
	
@example:
	python sigCheck.py sig_folder insert.sig
	
"""
import sys
from os.path import join
from os import listdir, rename
import numpy as np
from shutil import copy 
root = sys.argv[1]
miss = sys.argv[-1]
def check(root):
	folderList = listdir(root)
	for folder in folderList:
		if folder[0] == '.':
			continue
		
		fileList = listdir('./'+root+'/'+folder)
		timeSeq = []
		for files in fileList:
			segs = files.split('.')
			try:
				if segs[1] == 'sig':
					segs = segs[0].split('_')
					intSegs = int(segs[-1])
					timeSeq.append(intSegs)
			except:
				pass
		timeSeq = np.sort(timeSeq)
		digi = np.floor(np.log10(max(timeSeq)))+1
		digi_len = '%0'+str(digi)+'d'
		
		if len(timeSeq)==0:
			print folder
			continue
		
		if digi>3:
			for file in fileList:
				trackName = file.split('_')[0]
				trackNum = int(file.split('_')[1].split('.')[0])
				newname = trackName+'_'+digi_len%trackNum+'.sig'
				print root+"/"+folder+"/"+file
				rename(root+folder+"/"+file, root+"/"+folder+"/"+newname)
	
		timeStr = [digi_len%i for i in timeSeq]
		number = [digi_len%i for i in range(0,max(timeSeq))]
		
		for n in number:
			if n not in timeStr:
				print root+'/'+folder+'/'+folder+'_'+n+'.sig'
				copy(miss,root+'/'+folder+'/'+folder+'_'+n+'.sig')
if __name__ == '__main__':
	check(root)
