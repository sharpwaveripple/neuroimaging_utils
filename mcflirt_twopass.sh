#!/bin/bash

# NOTE: Because it's MCFLIRT, OMIT FILE EXTENSIONS!!

raw_func=$1

echo "Calculating first pass with $raw_func..."

mcflirt -in $raw_func \
  -out first_pass \
  -stages 4 \
  -meanvol \
  -spline_final \
  -report

fslmaths first_pass -Tmean first_pass_mean

echo "Calculating second pass with $raw_func..."

mcflirt -in $raw_func \
  -reffile first_pass_mean \
  -stages 4 \
  -spline_final \
  -plots \
  -report

fslmaths ${raw_func}_mcf.nii.gz -Tmean ${raw_func}_mcf_mean.nii.gz

rm first_pass.nii.gz first_pass_mean.nii.gz
