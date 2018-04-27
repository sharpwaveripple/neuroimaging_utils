#!/bin/bash

# INPUT: Low-res func
# INPUT2: High-res anat
# INPUT3: Forward transform file
# INPUT4: Inverse transform file
# OUTPUT: Forward and inverse transforms between spaces in transform dir

# Simply wraps calls to fsl utils

func=$1
anat=$2
forward_xfm=$3
backward_xfm=$4

echo "Using FLIRT to register $func to $anat..."

flirt \
  -datatype double \
  -in $func \
  -ref $anat \
  -omat $forward_xfm

echo "Inverting $forward_xfm with convert_xfm..."

convert_xfm \
  -omat $backward_xfm \
  -inverse $forward_xfm

echo "Saved $backward_xfm"
