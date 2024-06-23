#attension, the contour input dimension there are (zdim,xdim,ydim) instead of (xdim,ydim,zdim)
import nibabel as nib
import numpy as np
import pandas as pd
from scipy.ndimage import zoom
import os

def resample_image_with_voxel(input_path, output_path, original_voxel_size, new_voxel_size=(1, 1, 1)):
    img = nib.load(input_path)
    data = img.get_fdata()
    original_affine = img.affine

    rescaling_factors = np.array(original_voxel_size) / np.array(new_voxel_size)

    new_data = zoom(data, rescaling_factors, order=0)  # order=0 for nearest neighbor interpolation (good for binary masks)

    new_affine = np.copy(original_affine)
    np.fill_diagonal(new_affine, np.append(new_voxel_size, 1))

    new_img = nib.Nifti1Image(new_data, new_affine)

    nib.save(new_img, output_path)
    print(f"Resampled image saved to: {output_path}")

def clean_voxel_size(voxel_size_str):
    cleaned_str = voxel_size_str.replace('(', '').replace(')', '').replace(' ', '')
    size_components = cleaned_str.split(',')
    return [float(size) for size in size_components]

def main(contour_dir, output_dir, csv_path):
    df = pd.read_csv(csv_path)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for _, row in df.iterrows():
        patient_name = row[0]
        voxel_size_str = row[2]

        voxel_size = clean_voxel_size(voxel_size_str)

        input_path = os.path.join(contour_dir, f"{patient_name}_PT.nii.gz")
        output_path = os.path.join(output_dir, f"{patient_name}_PT.nii.gz")

        if os.path.exists(input_path):

            resample_image_with_voxel(input_path, output_path, original_voxel_size=voxel_size)
        else:
            print(f"Input file not found: {input_path}")

contour_directory = '/RadOnc-MRI1/Student_Folder/tangzx/Data/private_data_head_neck/labelsTr_nii'
output_directory = '/RadOnc-MRI1/Student_Folder/tangzx/Data/resample/contour'
csv_file_path = '/RadOnc-MRI1/Student_Folder/tangzx/Data/private_data_head_neck/voxel_swap.csv'

main(contour_directory, output_directory, csv_file_path)
