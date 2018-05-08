#!/usr/bin/env python 

import argparse
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt


def pick_slices(x, y, total_slices):
    step_sz = total_slices // (x*y)
    slices = list(range(step_sz//2, total_slices+1, step_sz))
    return slices


def slice_img(img, slice_num, slice_axis):
    sliced_img = np.take(img, slice_num, axis=slice_axis)
    oriented_slice = np.flipud(sliced_img.T)
    return oriented_slice


def stack_slices(img, slices, x, y, slice_axis):
    # need to concatenate these in opposite order for FS!
    ind = 0
    for i in range(y):
        for j in range(x):
            slice_num = slices[ind]
            if j == 0:
                row_img = slice_img(img, slice_num, slice_axis)
            else:
                row_img = np.hstack((row_img, slice_img(img, slice_num,
                                                        slice_axis)))
            ind += 1
        if i == 0:
            col_img = row_img
        else:
            col_img = np.vstack((col_img, row_img))
    return col_img


def save_figure(filename, quality):
    if quality == "low":
        output_dpi = 100
    elif quality == "high":
        output_dpi = 300
    else:
        output_dpi = 200
    plt.savefig(filename, dpi=output_dpi, bbox_inches="tight", pad_inches=0)


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
    parser.add_argument("--quality",
                        type=str, required=False, default="medium", metavar="",
                        help="Quality of output figure (low/{medium}/high)")
    args = parser.parse_args()
    return args


def io_stream():
    args = parse_input()
    base = nib.load(args.anat)
    overlay = nib.load(args.mask)
    if isinstance(base, nib.freesurfer.MGHImage):
        slice_axis = 1
    else:
        slice_axis = 2
    # note that conformed space is 256 isotropic, so special case
    slices = pick_slices(args.x, args.y, base.shape[0])
    base_img = stack_slices(base.get_data(), slices, args.x, args.y, slice_axis)
    overlay_img = stack_slices(overlay.get_data(), slices, args.x, args.y,
                               slice_axis)
    plt.imshow(base_img, cmap="gray")
    if len(np.unique(overlay)) > 2:
        plt.imshow(overlay_img, cmap="nipy_spectral", alpha=0.35)
    else:
        plt.imshow(overlay_img, cmap="plasma", alpha=0.35)
    plt.axis("off")
    # plt.show()
    save_figure(args.output, args.quality)


if __name__ == "__main__":
    io_stream()

