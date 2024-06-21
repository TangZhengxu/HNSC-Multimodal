import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np

def visualize_nifti(nifti_file_path):
    # Load the nii file
    nifti_img = nib.load(nifti_file_path)

    image_data = nifti_img.get_fdata()
    
    # slice for visualization
    middle_slice = image_data.shape[2] // 2
    
    plt.figure(figsize=(8, 8))
    plt.imshow(image_data[:, :, middle_slice], cmap="gray")
    plt.title(f'Middle Slice of {nifti_file_path}')
    plt.axis('off')
    plt.show()

nifti_file_path = '/RadOnc-MRI1/Student_Folder/tangzx/Data/private_data_head_neck/mri_post_vp/UM01_post_vp.nii'
visualize_nifti(nifti_file_path)
