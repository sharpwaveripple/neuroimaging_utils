#!/usr/bin/env python

import argparse
import numpy as np
import nibabel as nib
from scipy import stats

parser = argparse.ArgumentParser(description="""Extract functional connectivity network
using an input 4D functional image and 3D atlas""")

parser.add_argument("input", metavar="input",
                    help="Path to input 4D image (should be .nii.gz)")
parser.add_argument("output", metavar="output",
                    help="Output functional connectivity matrix (.csv)")
parser.add_argument("atlas", metavar="atlas",
                    help="3D atlas image registered to input image")
parser.add_argument("--zero_anticorrelations", action='store_true',
                    help="Zero significantly negative correlations")
args = parser.parse_args()

# Load data and infer properties
func_data = nib.load(args.input).get_data()
aparc_data = nib.load(args.atlas).get_data()
n_nodes = len(np.unique(aparc_data)) - 1
n_vols = func_data.shape[-1]


# Extract mean BOLD signal per ROI for the time series
mean_signal = np.empty((n_nodes, n_vols))
for i in range(1, n_nodes + 1):
    for j in range(n_vols):
        mean_signal[i-1, j] = np.mean(func_data[:, :, :, j][aparc_data==i])


# Compute the resting-state correlation matrix
corrmat = np.empty((n_nodes, n_nodes))
for i in range(n_nodes):
    for j in range(n_nodes):
        r, p = stats.pearsonr(mean_signal[i], mean_signal[j])

        # Zero significantly negative correlations
        if args.zero_anticorrelations and r < 0 and p < 0.05:
            r = 0

        corrmat[i, j] = r


# Compute Fisher's r-to-z transform (equal to arctanh)
np.fill_diagonal(corrmat, 0)
corrmat = np.arctanh(corrmat)

# Save matrix as csv with 16 digit precision
np.savetxt(args.output, corrmat, fmt='%.16f', delimiter=',')
