#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 14:25:53 2019
Updated on Sun Oct 13 17:11:36 2019
Updated on Tue Feb 23 15:22:38 2021

This is used to output the prerequisites for some volumetric analyses off of 
nii / nii.gz / voi files.  First, this renames .voi files (from mricron tracing )
to .nii.gz, since that is what they are. Then it opens all the .nii.gz and nii 
files in the same directory as the script and will write out a file with their
names, the sum of all the voxels in the file, and number of non-zero voxels in
the files, and the voxel x y and z size in mm.

Updated - Will now support label masks, counting the number of voxels with each 
integer label up to 128. Flexible by changing the maxLabelInt

TODO really would be better to also output to json or something like that?

@author: fordb
"""

import os
from  os.path import join
import nibabel as nib
import numpy as np
import csv
import datetime 

Path = "/media/fordb/scratch/2021-retro-python/2021-03-04_t2smoothing_gibbs/"
filelist = os.listdir(Path)
os.chdir(Path)
maxLabelInt = 6

output = [["File","Sum","Count_nonzero","VoxSize X mm","VoxSize Y mm","VoxSize Z mm"]]

#This is good for masked i.e. whole-number volumes, not for floats
#for label in range(maxLabelInt):
#    output[0].append(str(label) + " count")

for x in range(len(filelist)):
    file = filelist[x]
    if file.endswith(".voi"):
        try:    
            filename_without_ext = os.path.splitext(file)[0]
            new_file_name_with_ext = filename_without_ext+".nii.gz"
            print("changing extension of: " + x + " to .nii.gz")
            os.rename(join(Path,x),join(Path,new_file_name_with_ext))
            filelist[x] = new_file_name_with_ext
            file = new_file_name_with_ext
        except:
            pass
    if (file.endswith(".nii.gz") or file.endswith(".nii")):
        img = nib.load(file)
        header = img.header
        data = img.get_fdata()
        if len(data.shape) == 3:
            #This gets the voxel sizes in mms
            voxd = header.get_zooms()
            output.append([os.path.splitext(file)[0] , sum(sum(sum(data))) , np.count_nonzero(data) , voxd[0] , voxd[1] , voxd[2]])
            unique, counts = np.unique(data, return_counts=True)
            #uniqueCounts = dict(zip(unique, counts))
            #This is really better suited to a flexible format (e.g. json) as opposed to the rectangular table/csv expectation.
            #for label in range(maxLabelInt+1):
            #    try:
            #        output[len(output)-1].append(uniqueCounts[label])
            #    except:
            #        output[len(output)-1].append(None)
            print(os.path.splitext(file)[0] + " processed")
        else:
            print(os.path.splitext(file)[0] + " does not appear to be 3-dimensionsal, skipping")
        
      
now = datetime.datetime.now()
nowfile = now.strftime("%Y%m%d%H%M")
print("Writing " + str(len(output)-1) + " files worth of volumes to nii_file_sizer" + nowfile + ".csv")        
with open("nii_file_sizer" + nowfile + ".csv", 'w') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerows(output)
writeFile.close()
