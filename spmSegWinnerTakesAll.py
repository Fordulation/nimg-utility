#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 12:11:04 2022

Takes spm's segmentation outputs (c1, c2, c3, c4, c5) and combines them into
a single winnter-takes-all image
takes one argument, which should be the c1 file
@author: fordb
"""

import nibabel as nib 
import sys
import os 
import numpy as np

def usage():
    print(
        "This combines the separate SPM segmentation images (c1, c2, c3, c4, c5) into a "
        "single, winnter-takes-all image.\n\nUSAGE:\npython spmSegWTA.py <c1ImageFromSPM.nii>"
        "\n\nThe c1 image from SPM should be in the same directory as the c2, c3, c4, and c5 images"
        )


def finderrsinfile (cpath, cfile):
    noerrors = True
    if not (cfile.endswith(".nii") or cfile.endswith(".nii.gz")):
        print("ERROR: " + cfile + " does not end with .nii or .nii.gz.")
        noerrors = False
    if not (cfile.startswith("c1")):
        print("ERROR: " + cfile + " does not start with 'c1'.")
        noerrors = False
    if noerrors:
        #now check if files exist
        if not os.path.exists(os.path.join(cpath,cfile)):
            print("ERROR: " + os.path.join(cpath,cfile) + " does not exist.")
            noerrors = False
        c2 = cfile.replace('c1','c2')
        if not os.path.exists(os.path.join(cpath,c2)):
            print("ERROR: " + os.path.join(cpath,c2) + " does not exist.")
            noerrors = False
        c3 = cfile.replace('c1','c3')
        if not os.path.exists(os.path.join(cpath,c3)):
            print("ERROR: " + os.path.join(cpath,c3) + " does not exist.")
            noerrors = False
        c4 = cfile.replace('c1','c4')
        if not os.path.exists(os.path.join(cpath,c4)):
            print("ERROR: " + os.path.join(cpath,c4) + " does not exist.")
            noerrors = False
        c5 = cfile.replace('c1','c5')
        if not os.path.exists(os.path.join(cpath,c5)):
            print("ERROR: " + os.path.join(cpath,c5) + " does not exist.")
            noerrors = False
    return noerrors


def main():
    if len(sys.argv) < 2:
        usage()
    else:
        path, file = os.path.split(sys.argv[1])
        noerrors = finderrsinfile(path,file)
        if noerrors:
            c1img = nib.load(os.path.join(path,file))
            c1data = c1img.get_fdata()
            c2img = nib.load(os.path.join(path,file.replace('c1','c2')))
            c2data = c2img.get_fdata()
            c3img = nib.load(os.path.join(path,file.replace('c1','c3')))
            c3data = c3img.get_fdata()
            c4img = nib.load(os.path.join(path,file.replace('c1','c4')))
            c4data = c4img.get_fdata()
            c5img = nib.load(os.path.join(path,file.replace('c1','c5')))
            c5data = c5img.get_fdata()
            
            cxdata = np.stack([np.zeros_like(c1data), c1data, c2data, c3data, c4data, c5data],axis=-1)
            wta_data = np.argmax(cxdata, axis=3)
            
            wta_img = nib.Nifti1Image(wta_data, c1img.affine, c1img.header)
            wta_name = file.replace('c1','cx')
            print("Writing winner-take-all tissue class file to " + os.path.join(path,wta_name))
            nib.save(wta_img, os.path.join(path,wta_name))
main()