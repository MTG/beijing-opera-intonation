import yaml

annotations = yaml.load(file("annotations.yaml"))
MBIDs = annotations.keys()
for MBID in MBIDs:
	print "../database/wav/"+MBID+".wav"
