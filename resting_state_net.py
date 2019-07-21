#!/usr/bin/env python3

import argparse
import numpy as np
import nibabel as nib

def parse_input():
    parser = argparse.ArgumentParser(description='''Python script for
                                     extracting resting-state correlation matrices
                                     using an atlas''')
    parser.add_argument("-i", required=True, type=str, help="Input image")
    parser.add_argument("-o", required=True, type=str, help="Output matrix")
    parser.add_argument("-atlas", required=True, type=str,
                        help="Atlas file in functional space")
    args = parser.parse_args()
    return args

args = parse_input()
func = args.i
atlas = args.atlas
output = args.o

print(f"Reading functional data from {func}...")
func_data = nib.load(func).get_data()
print(f"Reading atlas from {atlas}...")
atlas_data = nib.load(atlas).get_data()
n_nodes = len(np.unique(atlas_data)) - 1 # due to 0 being a unique value
n_vols = np.shape(func_data)[3]
print(f"Correlating {n_nodes} nodes across {n_vols} volumes...")

a = np.full([n_vols, n_nodes], np.nan)

col = 0
for i in range(1, n_nodes+1):
    idx = np.where(atlas_data==i)
    row = 0
    for j in range(0, n_vols):
        func_slice = func_data[:, :, :, j]
        mean_val = np.mean(func_slice[idx])
        a[row, col] = mean_val
        row += 1
    col += 1

corrmat = np.full([n_nodes, n_nodes], np.nan)
for i in range(0, n_nodes):
    node1 = a[:, i]
    for j in range(i+1, n_nodes):
        node2 = a[:, j]
        r = np.corrcoef(node1, node2)[0, 1]
        corrmat[i, j] = r
        corrmat[j, i] = r

np.fill_diagonal(corrmat, 0)

print(f"Saving results to {output}...")
np.savetxt(output, corrmat, fmt="%.12f", delimiter="\t")
