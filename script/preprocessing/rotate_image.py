#counter colckwise 90 degree, duicheng y axis
import SimpleITK as sitk
import numpy as np
import os

def load_nii(file_path):
    return sitk.ReadImage(file_path)

def save_nii(image, file_path):
    sitk.WriteImage(image, file_path)

def process_data(image):
    data = sitk.GetArrayFromImage(image)

    data_rotated = np.rot90(data, k=1, axes=(1, 2))
    data_flipped = np.flip(data_rotated, axis=1)

    processed_image = sitk.GetImageFromArray(data_flipped)

    processed_image.SetSpacing(image.GetSpacing())
    processed_image.SetOrigin(image.GetOrigin())
    processed_image.SetDirection(image.GetDirection())

    return processed_image

def process_all_files(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith(".nii"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)

            input_image = load_nii(input_path)

            processed_image = process_data(input_image)

            save_nii(processed_image, output_path)

            print(f"Processed {filename} and saved to {output_path}")

input_directory = '/RadOnc-MRI1/Student_Folder/tangzx/Data/resample/pre_t1' 
output_directory = '/RadOnc-MRI1/Student_Folder/tangzx/Data/resample/pre_t1_rotate' 

process_all_files(input_directory, output_directory)
