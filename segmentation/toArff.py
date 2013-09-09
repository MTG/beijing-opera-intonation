#!/usr/bin/env python

from mutagen.id3 import ID3
import os
import sys

collection_root = sys.argv[1]

def convert(filepath):
    print 'python essentiaToWeka.py '+filepath

def walkDirs(root):
    for (path, dirs, files) in os.walk(root):
        for f in files:
            if ".sig" in f.lower():
                convert(path)
		break

if __name__ == "__main__":
    walkDirs(collection_root)
