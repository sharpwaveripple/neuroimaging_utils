import argparse
import nibabel as nib


def io_stream():
    args = parse_input()
    dropped_vols = drop_initial_nvols(args.i, args.nvols)
    dropped_vols.to_filename(args.o)


def parse_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", type=str, required=True,
                        help="Input file")
    parser.add_argument("-o", type=str, required=True,
                        help="Output file")
    parser.add_argument("-nvols", type=int, required=True,
                        help="Number of initial volumes to drop")
    args = parser.parse_args()
    return args


def drop_initial_nvols(nii_path, nvols):
    data = nib.load(nii_path)
    affine = data.get_affine()
    header = data.header.copy()
    steady_state_vols = data.dataobj[..., nvols:]
    img = nib.Nifti1Image(steady_state_vols, affine, header=header)
    return img


if __name__ == "__main__":
    io_stream()
