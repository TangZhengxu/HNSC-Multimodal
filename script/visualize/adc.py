import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np

# Path to the nii file
nifti_file_path = '/RadOnc-MRI1/Student_Folder/tangzx/Data/private_data_head_neck/mri_post_adc/UM01_post_adc.nii'

nifti_img = nib.load(nifti_file_path)
nifti_data = nifti_img.get_fdata()

#slice to display
slice_index = nifti_data.shape[2] // 2  # Middle slice

plt.figure(figsize=(8, 8))
plt.imshow(nifti_data[:, :, slice_index], cmap='gray', origin='lower')
plt.title(f'Slice {slice_index}')
plt.axis('off')
plt.show()
