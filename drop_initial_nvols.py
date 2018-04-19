#!/usr/bin/env python

import argparse
import nibabel as nib


def io_stream():
    args = parse_input()
    dropped_vols = drop_initial_nvols(args.i, args.nvols)
    print(f"Saving as {args.o}...")
    dropped_vols.to_filename(args.o)
    print("Done")


def set_output_name(source_nii, nvols):
    return source_nii.rstrip(".nii.gz") + f"_drop{nvols}"


def parse_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", type=str, required=True,
                        help="Input file")
    parser.add_argument("-o", type=str,
                        help="Output file")
    parser.add_argument("-nvols", type=int, default=4,
                        help="Number of initial volumes to drop")
    args = parser.parse_args()
    if args.o is None:
        args.o = set_output_name(args.i, args.nvols)
    if not args.o.endswith((".nii", ".nii.gz")):
        args.o += ".nii.gz"
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
