# -*- coding: utf-8 -*-

"""
The extractFeatures.py will create a folder for each audio file, when want to create a single arff file from multi-folders, using this script to move .sig files together. If the destination folder doesn't exist, it will be created automatically.
	
Example: 
	Move all the *.sig files in orignal_folder to destination_folder
	python original_folder destination_folder

@author: Kainan Chen
"""

from os import mkdir
from os.path import walk, exists
from shutil import copyfile
import sys

def sigComb(destFolder, oriFolder, fnames):
	for fname in fnames:
		if fname[-4:]=='.sig':
			copyfile(oriFolder+"/"+fname,destFolder+"/"+fname)


if __name__ == '__main__':
	oriFolder = sys.argv[1]
	destFolder = sys.argv[-1]
	if not exists(destFolder):
		mkdir(destFolder)
	print oriFolder,destFolder
	walk(oriFolder, sigComb, destFolder)
	print "Done!"
