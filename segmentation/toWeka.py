from os import listdir
import sys

root = sys.argv[1]
folderList = listdir(root)
for folders in folderList:
	if folders[0] != '.':
		print 'python essentiaToWeka.py ' + root + folders
