import os
import nibabel as nib
import numpy as np
from scipy.ndimage import zoom

def resample_adc_image(input_path, output_path, new_voxel_size=(1, 1, 1)):
    # Load the original ADC image
    img = nib.load(input_path)
    data = img.get_fdata()
    original_affine = img.affine

    # Compute the rescaling factor
    original_voxel_size = np.linalg.norm(original_affine[:3, :3], axis=0)
    rescaling_factors = original_voxel_size / np.array(new_voxel_size)

    # Ensure rescaling factors match the number of dimensions
    if len(data.shape) > 3:
        rescaling_factors = list(rescaling_factors) + [1] * (len(data.shape) - 3)

    # Resample the ADC image
    new_data = zoom(data, rescaling_factors, order=1)  # order=1 for linear interpolation

    # Compute the new affine matrix
    new_affine = np.copy(original_affine)
    np.fill_diagonal(new_affine, np.append(new_voxel_size, 1))

    # Create a new nii image
    new_img = nib.Nifti1Image(new_data, new_affine)

    # Save the resampled image
    nib.save(new_img, output_path)
    print(f"Resampled ADC image saved to: {output_path}")

def resample_all_files_in_folder(input_folder, output_folder, new_voxel_size=(1, 1, 1)):
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.endswith('.nii') or filename.endswith('.nii.gz'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            resample_adc_image(input_path, output_path, new_voxel_size)

input_folder = '/RadOnc-MRI1/Student_Folder/tangzx/Data/private_data_head_neck/mri_pre_adc'
output_folder = '/RadOnc-MRI1/Student_Folder/tangzx/Data/resample/pre_adc/'
resample_all_files_in_folder(input_folder, output_folder)
