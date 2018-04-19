#!/bin/bash

T1=$1
TPM1=$2
TPM2=$3
TPM3=$4
T1_brain=$5

fslmaths $TPM1 -add $TPM2 -add $TPM3 bin_brain.nii.gz
fslmaths $T1 -mas bin_brain.nii.gz $T1_brain
rm bin_brain.nii.gz 

N4BiasFieldCorrection \
  -d 3 \
  -v \
  -i $T1_brain \
  -o $T1_brain
