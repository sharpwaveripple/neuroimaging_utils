#!/usr/bin/env python3

import subprocess
import argparse
import numpy as np
import nibabel as nib

# https://www.jiscmail.ac.uk/cgi-bin/webadmin?A2=FSL;641b2f2d.0912
# https://www.jiscmail.ac.uk/cgi-bin/webadmin?A2=fsl;fc5b33c5.1205

def hz_to_sigma(tr, freq):
    sigma = 1 / (2 * tr * freq)
    return sigma

def parse_input():
    parser = argparse.ArgumentParser(description='''Python wrapper for
                                     fslmaths -bptf, using input in Hz''')
    parser.add_argument("-i", required=True, help="Input image")
    parser.add_argument("-o", required=True, help="Output image")
    parser.add_argument("-mean_func", type=str, required=True,
                        help="Mean func file produced using fslmaths -Tmean")
    parser.add_argument("-tr", type=float, required=True, help="TR in seconds")
    parser.add_argument("-hp", type=float, default=-1, help="Highpass cutoff in Hz")
    parser.add_argument("-lp", type=float, default=-1, help="Lowpass cutoff in Hz")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_input()
    if args.hp > 0:
        hp = hz_to_sigma(args.tr, args.hp)
    else:
        hp = args.hp
    if args.lp > 0:
        lp = hz_to_sigma(args.tr, args.lp)
    else:
        lp = args.lp
    cmdarg = ['fslmaths', args.i, '-bptf', str(hp), str(lp), 
              '-add', args.mean_func, args.o]
    print(cmdarg)
    subprocess.run(cmdarg)
