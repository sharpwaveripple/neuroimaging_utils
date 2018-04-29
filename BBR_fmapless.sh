#!/bin/bash

# INPUT1: Mean func to register
# INPUT2: Raw anat
# INPUT3: Brain extracted anat
# INPUT4: White matter seg
# INPUT5: Output basename
# INPUT6: Inverse output matrix

# OUTPUT: BBR transform and its inverse

epi=$1
t1=$2
t1brain=$3
wmseg=$4
out=$5
out_inv=$6

out_file=$(basename $out)
out_dir=$(dirname $out) 
expected_wmseg=$out_dir/${out_file}_fast_wmseg.nii.gz
wmedge=$out_dir/${out_file}_fast_wmedge.nii.gz

if [ $wmseg != $expected_wmseg ]; then
  echo "$wmseg doesn't follow FSL convention, copying as $expected_wmseg"
  cp $wmseg $expected_wmseg
fi

epi_reg --epi=$epi --t1=$t1 --t1brain=$t1brain --out=$out --wmseg=$wmseg -v

echo "Saving inverse of $out as $out_inv..."
convert_xfm -omat ${out_inv} -inverse ${out}.mat

echo "Removing redunant files..."
rm ${out}.nii.gz $out_dir/${out_file}_init.mat
rm $wmedge            # Might be useful for tractography...
if [ $wmseg != $expected_wmseg ]; then
  rm $expected_wmseg
fi
