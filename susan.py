#!/usr/bin/env python3

import subprocess
import argparse
import numpy as np
import nibabel as nib

def susan_parameters(nii, fwhm):
    data = nib.load(nii).get_data()
    bt = (np.median(data[data != 0]) - np.percentile(data, 2)) * 0.75
    dt = fwhm / 2.355
    return bt, dt


def parse_input():
    parser = argparse.ArgumentParser(description='''Spatial smoothing using FSL SUSAN.
                                     Implementation based on 
                                     https://www.jiscmail.ac.uk/cgi-bin/webadmin?A2=FSL;d23aeab5.1004''')

    parser.add_argument("-i", type=str, required=True, help="Input file")
    parser.add_argument("-o", type=str, required=True, help="Output file")
    parser.add_argument("-fwhm", type=float, default=6.0, required=True,
                        help="Smoothing kernel in FWHM (mm)")
    parser.add_argument("-mean_func", type=str, required=True,
                        help="Mean func file produced using fslmaths -Tmean")
    args = parser.parse_args()
    if not args.o.endswith((".nii", ".nii.gz")):
        args.o += ".nii.gz"
    return args

if __name__ == "__main__":
    args = parse_input()
    bt, dt = susan_parameters(args.i, args.fwhm)
    cmdarg = ['susan', args.i, str(bt), str(dt), '3', '1', '1', 
              args.mean_func, str(bt), args.o]
    print(cmdarg)
    subprocess.run(cmdarg)

