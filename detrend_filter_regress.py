#!/usr/bin/env python

import argparse
import numpy as np
from nilearn.image import clean_img

parser = argparse.ArgumentParser(description="CLI to nilearn.image.clean_img")
parser.add_argument("input", metavar="input",
                    help="Path to input 4D image (should be .nii.gz)")
parser.add_argument("output", metavar="output",
                    help="Output filtered 4D image (should be .nii.gz)")
parser.add_argument("-high_pass", type=float, default=None, metavar="",
                    help="Highpass cutoff in Hz (Standard value: 0.009)")
parser.add_argument("-low_pass", type=float, default=None, metavar="",
                    help="Lowpass cutoff in Hz (Standard value: 0.08)")
parser.add_argument("-t_r", type=float, metavar="",
                    help="TR in seconds")
parser.add_argument("-confounds", type=str, default=None, metavar="",
                    help="Path to text file with confounds")
parser.add_argument("--detrend", action='store_true',
                    help="Remove linear trends")
parser.add_argument("--standardize", action='store_true',
                    help="Standardize to unit variance")
args = parser.parse_args()

detrend = args.detrend
standardize = args.standardize
high_pass = args.high_pass
low_pass = args.low_pass
t_r = args.t_r

if (high_pass or low_pass) and t_r is None:
    raise ValueError("Please specify -t_r for temporal filtering operations")

if (high_pass and low_pass) and high_pass >= low_pass:
    raise ValueError(f"""High pass cutoff ({high_pass}) >= \
low pass cutoff ({low_pass})""")

if args.confounds:
    confounds = np.loadtxt(args.confounds)
    print(f"{args.confounds} loaded as confounds with shape {confounds.shape}")

filtered_img = clean_img(args.input, detrend=detrend, standardize=standardize,
                         low_pass=low_pass, high_pass=high_pass, t_r=t_r,
                         confounds=confounds)

filtered_img.to_filename(args.output)
