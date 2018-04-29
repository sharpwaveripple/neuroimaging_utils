#!/bin/bash

# INPUT: Raw functional to be motion corrected
# OUTPUT: Two pass motion corrected file in the same folder

func=$1

func_file=$(basename $func .nii.gz)
func_dir=$(dirname $func) 
mcf_func=$func_dir/${func_file}_mcf
first_pass=$func_dir/first_pass 
first_pass_mean=$func_dir/first_pass_mean

echo "Calculating first pass with $func..."

mcflirt -in $func \
  -out $first_pass \
  -stages 4 \
  -meanvol \
  -spline_final \
  -report

fslmaths $first_pass -Tmean $first_pass_mean

echo "Calculating second pass with $func_file..."

mcflirt -in $func \
  -out $mcf_func \
  -reffile $first_pass_mean \
  -stages 4 \
  -spline_final \
  -plots \
  -report

echo "Taking temporal mean of $mcf_func..."

fslmaths $mcf_func -Tmean ${mcf_func}_mean

rm ${first_pass}.nii.gz ${first_pass_mean}.nii.gz 
