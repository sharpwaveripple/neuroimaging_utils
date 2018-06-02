#!/bin/bash

# note that this probably isn't POSIX compatible.

probtrack_dir=${1}
cd $probtrack_dir

if [[ ! -e fdt_matrix2_lengths.dot ]]; then
  echo "No length matrix found! Aborting!"
  exit 1
fi

paste -d '  ' <(cat fdt_matrix2.dot | tr -s " ") \
  <(cut -d ' ' -f 5 fdt_matrix2_lengths.dot) \
  > fdt_matrix2_combined.dot

rm \
  fdt_matrix2.dot \
  fdt_matrix2_lengths.dot \
  lookup_tractspace_fdt_matrix2.nii.* \
  fdt_paths.nii.gz \
  fdt_paths_lengths.nii.gz
