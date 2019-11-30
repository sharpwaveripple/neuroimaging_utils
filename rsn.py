#!/usr/bin/env python

import sys
import numpy as np
import nibabel as nib
from scipy import stats


# Load data and infer properties
in_func = sys.argv[1]
atlas = sys.argv[2]
out_mat = sys.argv[3]

func_data = nib.load(in_func).get_data()
aparc_data = nib.load(atlas).get_data()
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
        if r < 0 and p < 0.05:
            r = 0
        corrmat[i, j] = r


# Compute Fisher's r-to-z transform (equal to arctanh)
np.fill_diagonal(corrmat, 0)
corrmat = np.arctanh(corrmat)


# Save matrix as csv with 16 digit precision
np.savetxt(out_mat, corrmat, fmt='%.16f', delimiter=',')
