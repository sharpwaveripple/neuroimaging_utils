#!/usr/bin/env python

import sys
import numpy as np
import nibabel as nib

in_func = sys.argv[1]
atlas = sys.argv[2]
out_mat = sys.argv[3]

func_data = nib.load(in_func).get_data()
aparc_data = nib.load(atlas).get_data()

n_nodes = len(np.unique(aparc_data)) - 1
n_vols = func_data.shape[-1]

x = np.empty((n_nodes, n_vols))
for i in range(1, n_nodes + 1):
    for j in range(n_vols):
        x[i-1, j] = np.mean(func_data[:, :, :, j][aparc_data==i])

corrmat = np.corrcoef(x)
np.fill_diagonal(corrmat, 0)

np.savetxt(out_mat, corrmat, fmt='%.16f', delimiter=',')
