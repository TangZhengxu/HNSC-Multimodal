import nibabel as nib
import numpy as np
from scipy.ndimage import zoom
import os

def resample_vp_image(input_path, output_path, new_voxel_size=(1, 1, 1)):
    # Loading the original VP image
    img = nib.load(input_path)
    data = img.get_fdata()
    original_affine = img.affine

    # Compute the original voxel size
    original_voxel_size = np.sqrt(np.sum(original_affine[:3, :3] ** 2, axis=0))

    # Compute the rescaling factor
    rescaling_factors = original_voxel_size / np.array(new_voxel_size)

    # Ensure rescaling factors match the number of dimensions
    rescaling_factors = np.append(rescaling_factors, np.ones(len(data.shape) - len(rescaling_factors)))

    # Resample the image
    new_data = zoom(data, rescaling_factors, order=1)  # order=1 for linear interpolation

    # Compute the new affine matrix
    new_affine = np.copy(original_affine)
    np.fill_diagonal(new_affine[:3, :3], new_voxel_size)

    # Create a new nii image
    new_img = nib.Nifti1Image(new_data, new_affine)

    # Save the resampled image
    nib.save(new_img, output_path)
    print(f"Resampled VP image saved to: {output_path}")

def resample_all_vp_images_in_folder(input_folder, output_folder, new_voxel_size=(1, 1, 1)):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in os.listdir(input_folder):
        if file_name.endswith('.nii') or file_name.endswith('.nii.gz'):
            input_path = os.path.join(input_folder, file_name)
            output_path = os.path.join(output_folder, file_name)
            resample_vp_image(input_path, output_path, new_voxel_size)

input_folder = '/RadOnc-MRI1/Student_Folder/tangzx/Data/private_data_head_neck/mri_pre_vp'
output_folder = '/RadOnc-MRI1/Student_Folder/tangzx/Data/resample/pre_vp/'
resample_all_vp_images_in_folder(input_folder, output_folder)
