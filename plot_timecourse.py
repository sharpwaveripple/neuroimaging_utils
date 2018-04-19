import matplotlib.pyplot as plt
import nibabel as nib

img = nib.load('001_rs_2011.nii.gz').get_data()
timecourse = img[42, 32, 19]
plt.plot(timecourse)
