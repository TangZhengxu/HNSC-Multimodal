import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np

# Load the nii file
nifti_file = '/RadOnc-MRI1/Student_Folder/tangzx/Data/private_data_head_neck/pet_post/UM45_post_pet.nii'
img = nib.load(nifti_file)
img_data = img.get_fdata()

def display_slices(slices):
    fig, axes = plt.subplots(1, len(slices))
    for i, slice in enumerate(slices):
        axes[i].imshow(slice.T, cmap="gray", origin="lower")
    plt.show()

slice_0 = img_data[img_data.shape[0] // 2, :, :]
slice_1 = img_data[:, img_data.shape[1] // 2, :]
slice_2 = img_data[:, :, img_data.shape[2] // 2]

display_slices([slice_0, slice_1, slice_2])
