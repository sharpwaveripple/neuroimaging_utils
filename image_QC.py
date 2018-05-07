#!/usr/bin/env python 

import argparse
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt


def pick_slices(x, y, total_slices):
    step_sz = total_slices // (x*y)
    slices = list(range(step_sz, total_slices+1, step_sz))
    return slices


def slice_img(img, slice_num):
    return np.flipud(img[:, :, slice_num].T)


def stack_slices(img, slices, x, y):
    ind = 0
    for i in range(y):
        for j in range(x):
            slice_num = slices[ind]
            if j == 0:
                row_img = slice_img(img, slice_num)
            else:
                row_img = np.hstack((row_img, slice_img(img, slice_num)))
            ind += 1
        if i == 0:
            col_img = row_img
        else:
            col_img = np.vstack((col_img, row_img))
    return col_img


def parse_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("--anat", type=str, required=True, metavar="",
                        help="Anatomical image (base)")
    parser.add_argument("--mask", type=str, required=True, metavar="",
                        help="Mask image (overlay)")
    parser.add_argument("--output", type=str, required=True, metavar="",
                        help="Output .png file")
    parser.add_argument("--x", type=int, required=False, default=5, metavar="",
                        help="Number of columns (default: 5)")
    parser.add_argument("--y", type=int, required=False, default=3, metavar="",
                        help="Number of rows (default: 3)")
    args = parser.parse_args()
    return args


def io_stream():
    args = parse_input()
    base = nib.load(args.anat).get_data()
    overlay = nib.load(args.mask).get_data()
    slices = pick_slices(args.x, args.y, base.shape[0])
    base_img = stack_slices(base, slices, args.x, args.y)
    overlay_img = stack_slices(overlay, slices, args.x, args.y)
    # turn into fx and guess if mask or parc or cont by datatype
    plt.imshow(base_img, cmap="gray")
    plt.imshow(overlay_img, cmap="plasma", alpha=0.35)
    plt.axis("off")
    # plt.show()
    plt.savefig(args.output, set_bbox_inches="tight")


if __name__ == "__main__":
    io_stream()

