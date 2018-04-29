#!/bin/bash

# INPUT1: Whole head T1
# INPUT2: Brain extracted T1
# INPUT3: T1 brain mask
# INPUT4: TPM1
# INPUT5: TPM2
# INPUT6: TPM3
# OUTPUT: Brain extracted T1

T1=$1
T1_brain=$2
T1_mask=$3
TPM1=$4
TPM2=$5
TPM3=$6

fslmaths $TPM1 -add $TPM2 -add $TPM3 -bin $T1_mask
fslmaths $T1 -mas $T1_mask $T1_brain
rm $T1_mask
