"""Script to expand regression parameters using backwards temporal difference 
and square with floating point precision"""

import argparse
import numpy as np


def expand_regressors():
    args = parse_input()
    confounds = normalise(square(derive_backwards(np.loadtxt(args.i))))
    np.savetxt(args.o, confounds, delimiter=' ', fmt='%f')


def parse_input():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-i", type=str, required=True,
                        help="Input file")
    parser.add_argument("-o", type=str, required=True,
                        help="Output file")
    args = parser.parse_args()
    return args


def normalise(mat):
    norm = (mat - np.mean(mat, axis=0)) / np.std(mat, axis=0)
    return norm

def derive_backwards(mat):
    first_diff = np.zeros(mat.shape[1])
    diff = mat[1:] - mat[:-1]
    td = np.vstack([first_diff, diff])
    return np.hstack([mat, td])

def square(mat):
    return np.hstack([mat, np.square(mat)])


if __name__ == "__main__":
    expand_regressors()
