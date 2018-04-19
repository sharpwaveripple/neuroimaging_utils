#!/usr/bin/env python

import argparse
import nibabel as nib


def io_stream():
    args = parse_input()
    dropped_vols = drop_initial_nvols(args.i, args.nvols)
    print(f"Saving to {args.o}...")
    dropped_vols.to_filename(args.o)
    print("Done")


def set_default_output(source_nii, nvols):
    basename = source_nii.rstrip(".nii.gz")
    out_vol = basename + f"_drop{nvols}" + ".nii.gz"
    return out_vol


def parse_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--in", metavar="\b", type=str, required=True,
                        help="Input file")
    parser.add_argument("-o", "--out", metavar="\b", type=str,
                        help="Output file")
    parser.add_argument("--nvols", type=int, metavar="\b", default=4,
                        help="Number of initial volumes to drop")
    args = parser.parse_args()
    if args.o is None:
        args.o = set_default_output(args.i, args.nvols)
    return args


def drop_initial_nvols(nii_path, nvols):
    print(f"Loading {nii_path}...")
    data = nib.load(nii_path)
    affine = data.get_affine()
    header = data.header.copy()
    print(f"Dropping first {nvols} volumes...")
    steady_state_vols = data.dataobj[..., nvols:]
    img = nib.Nifti1Image(steady_state_vols, affine, header=header)
    return img


if __name__ == "__main__":
    io_stream()
