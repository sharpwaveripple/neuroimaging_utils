subj=001_2011

fs_dir=/JT/FS/$subj
T1=$subj/${subj}_T1.nii.gz
T1_brain=$subj/${subj}_T1_brain.nii.gz
N4_brain=$subj/${subj}_T1_N4_brain.nii.gz
T1_mask=$subj/${subj}_T1_mask.nii.gz
DTI=$subj/${subj}_DTI_brain.nii.gz
b0=$subj/${subj}_DTI_b0.nii.gz

mri_dir=$fs_dir/mri
xfm_dir=$mri_dir/transforms
orig2raw=$xfm_dir/fs2anat.mat
bbr=$xfm_dir/dwi2anat
bbr_inv=$xfm_dir/anat2dwi.mat
fs2dwi=$xfm_dir/fs2dwi.mat

GM=$mri_dir/gm_T1.nii.gz
WM=$mri_dir/all-wm_T1.nii.gz
ventricles=$mri_dir/ventricles_T1.nii.gz

cerebellum_mask=$subj/${subj}_cerebellar_mask.nii.gz
output_DTI=DTI_DSEG/${subj}_DTI_nocerebellum.nii.gz

gen_tissue_masks.sh $fs_dir
cerebellum_mask.sh $fs_dir
orig2raw.sh $fs_dir $orig2raw
tissues_to_T1.sh $fs_dir $T1
TPM_brain_extraction.sh $T1 $T1_brain $T1_mask $GM $WM $ventricles

N4BiasFieldCorrection -d 3 -i $T1_brain -o $N4_brain -v

fslroi $DTI $b0 0 1
BBR_fmapless.sh $b0 $T1 $N4_brain $WM $bbr $bbr_inv
convert_xfm -omat $one_step_xfm -concat $bbr_inv $orig2raw

# interp=nearestneighbour
interp=spline

echo "Registering freesurfer to $DTI with $interp interpolation"

flirt \
  -datatype double \
  -interp $interp \
  -in $mri_dir/cerebellum.nii.gz \
  -ref $b0 \
  -applyxfm -init $fs2dwi \
  -out $cerebellum_mask

fslmaths $cerebellum_mask -thr 0.3 -bin $cerebellum_mask
fslmaths $DTI -mas $cerebellum_mask $output_DTI
