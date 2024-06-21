import nibabel as nib
import numpy as np
from scipy.ndimage import zoom
import os

def resample_image(input_path, output_path, new_voxel_size=(1, 1, 1)):
    # Load the original image
    img = nib.load(input_path)
    data = img.get_fdata()
    original_affine = img.affine

    # Compute the rescaling factor
    original_voxel_size = np.diag(original_affine)[:3]
    rescaling_factors = original_voxel_size / np.array(new_voxel_size)

    # Resample the image
    new_data = zoom(data, rescaling_factors, order=1)  # order=1 for linear interpolation

    # Compute the new affine matrix
    new_affine = np.copy(original_affine)
    np.fill_diagonal(new_affine, np.append(new_voxel_size, 1))

    # Create a new nii image
    new_img = nib.Nifti1Image(new_data, new_affine)

    # Save the resampled image
    nib.save(new_img, output_path)
    print(f"Resampled image saved to: {output_path}")

def resample_mri_files(input_dir, output_dir, new_voxel_size=(1, 1, 1)):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith('.nii') or filename.endswith('.nii.gz'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            resample_image(input_path, output_path, new_voxel_size)

input_directory = '/RadOnc-MRI1/Student_Folder/tangzx/Data/private_data_head_neck/mri_pre_t1_new'
output_directory = '/RadOnc-MRI1/Student_Folder/tangzx/Data/resample/pre_t1/'
resample_mri_files(input_directory, output_directory)
