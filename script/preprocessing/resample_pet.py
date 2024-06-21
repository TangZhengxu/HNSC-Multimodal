import nibabel as nib
import numpy as np
from scipy.ndimage import zoom
import os

def resample_image(input_path, output_path, new_voxel_size=(1, 1, 1)):
    # Load the original image
    img = nib.load(input_path)
    data = img.get_fdata()
    original_affine = img.affine

    # Debug: Print the original affine matrix
    #print("Original affine matrix for {}:\n{}".format(input_path, original_affine))

    # Compute the original voxel size
    original_voxel_size = np.sqrt(np.sum(original_affine[:3, :3] ** 2, axis=0))
    
    # Debug: Print the original voxel size
    #print("Original voxel size for {}: {}".format(input_path, original_voxel_size))

    # Compute the rescaling factor
    rescaling_factors = original_voxel_size / np.array(new_voxel_size)
    
    # Debug: Print the rescaling factors
    #print("Rescaling factors for {}: {}".format(input_path, rescaling_factors))

    # Ensure the rescaling factors are positive
    if np.any(rescaling_factors <= 0):
        raise ValueError("Rescaling factors must be positive. Check the original affine matrix and voxel sizes for {}.".format(input_path))

    # Debug: Print the shape of the data
    #print("Data shape for {}: {}".format(input_path, data.shape))

    # Handle cases where the data has an extra dimension
    if len(data.shape) == 4 and data.shape[3] == 1:
        data = data[:, :, :, 0]  # Remove the singleton dimension

    # Ensure the rescaling factors length matches the data dimensions
    if len(rescaling_factors) != len(data.shape):
        raise RuntimeError("The number of rescaling factors must match the number of dimensions of the data for {}.".format(input_path))

    # Resample the image
    new_data = zoom(data, rescaling_factors, order=1)  # order=1 for linear interpolation

    # Compute the new affine matrix
    new_affine = np.copy(original_affine)
    np.fill_diagonal(new_affine, np.append(new_voxel_size, 1))

    # Debug: Print the new affine matrix
    #print("New affine matrix for {}:\n{}".format(input_path, new_affine))

    # Create a new nii image
    new_img = nib.Nifti1Image(new_data, new_affine)

    # Save the resampled image
    nib.save(new_img, output_path)
    print(f"Resampled image saved to: {output_path}")

def resample_folder(input_folder, output_folder, new_voxel_size=(1, 1, 1)):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for file_name in os.listdir(input_folder):
        if file_name.endswith('.nii') or file_name.endswith('.nii.gz'):
            input_path = os.path.join(input_folder, file_name)
            output_path = os.path.join(output_folder, file_name)
            resample_image(input_path, output_path, new_voxel_size)

input_folder = '/RadOnc-MRI1/Student_Folder/tangzx/Data/private_data_head_neck/pet_pre'
output_folder = '/RadOnc-MRI1/Student_Folder/tangzx/Data/resample/pre_pet/'
resample_folder(input_folder, output_folder)
