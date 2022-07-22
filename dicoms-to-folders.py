#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 14:25:38 2022
sort a single folder with dicoms from many sequences into folders for each
sequence. Uses SequenceNumber from the dicom header to do so. 
@author: fordb
"""

import sys
import os 
import pydicom

def dicomsToFoldersUsage():
	print("This sorts dicoms from multiple series in a single directory into subdirectories for each series")
	print("Requires pydicom> acquire with pip install pydicom")
	print("Usage: python3 path/to/dicoms-to-folders.py directoryToProcess")
	print("E.g. python3 ./dicoms-to-folders.py /media/user/disk/study/dicoms")

if os.path.isdir(sys.argv[1]):
	path = sys.argv[1]
	filelist = os.listdir(path)
	print("Found " + str(len(filelist)) + " items.")
	if (len(filelist)>1):
		for file in filelist:
			if not os.path.isdir(os.path.join(path,file)):
				try:
					dicomdata = pydicom.dcmread(os.path.join(path,file))
					sn = str(dicomdata.SeriesNumber)
					if not os.path.isdir(os.path.join(path,sn)):
						os.mkdir(os.path.join(path,sn))
					os.rename(os.path.join(path,file),os.path.join(path,sn,file))
				except:
					print("Skipping " + file)
					pass
elif sys.argv[1] in ["--help" "-help" "-h" "--h"]:
	dicomsToFoldersUsage()
else:
	print("ERROR: "+sys.argv[1]+" is not a directory")
