# use it after resample!!!
import nibabel as nib
import numpy as np
import os

def change_nifti_dimensions(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    for file_name in os.listdir(input_folder):
        if file_name.endswith('.nii.gz'):
            input_path = os.path.join(input_folder, file_name)
            output_path = os.path.join(output_folder, file_name)

            nifti_image = nib.load(input_path)

            data = nifti_image.get_fdata()

            transposed_data = np.transpose(data, (1, 2, 0))

            new_nifti_image = nib.Nifti1Image(transposed_data, nifti_image.affine, nifti_image.header)

            nib.save(new_nifti_image, output_path)
            print(f"Saved new NIfTI image with dimensions {transposed_data.shape} to {output_path}")

input_folder = '/RadOnc-MRI1/Student_Folder/tangzx/Data/resample/contour'
output_folder = '/RadOnc-MRI1/Student_Folder/tangzx/Data/resample/contour_swap'
change_nifti_dimensions(input_folder, output_folder)
