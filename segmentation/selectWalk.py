from os import listdir

folderList = listdir('../ess_data')
for folders in folderList:
	if folders[0] != '.':
		fileList = listdir('../ess_data/'+folders)
		fnameList = ''
		for files in fileList:
			fnameList = fnameList + '../ess_data/'+folders+'/'+files+' '
		#	print 'python selectFeats_beijing_opera.py '+'./data/'+folders+'/'+files
		print 'python selectFeats.py ' +  fnameList
