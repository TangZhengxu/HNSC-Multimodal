import os
import shutil
from pathlib import Path
import numpy as np

# define input and output path
path_input_pet = Path("/RadOnc-MRI1/Student_Folder/tangzx/Data/private_data_head_neck/pet_pre")
path_input_t1 = Path("/RadOnc-MRI1/Student_Folder/tangzx/Data/private_data_head_neck/mri_pre_t1")
path_input_adc = Path("/RadOnc-MRI1/Student_Folder/tangzx/Data/private_data_head_neck/mri_pre_adc")
path_input_vp = Path("/RadOnc-MRI1/Student_Folder/tangzx/Data/private_data_head_neck/mri_pre_vp")
path_input_contour = Path("/RadOnc-MRI1/Student_Folder/tangzx/Data/private_data_head_neck/contour_pre")

path_output_images = Path("/RadOnc-MRI1/Student_Folder/tangzx/Data/private_data_head_neck/imagesTr")
path_output_labels = Path("/RadOnc-MRI1/Student_Folder/tangzx/Data/private_data_head_neck/labelsTr")

path_output_images.mkdir(parents=True, exist_ok=True)
path_output_labels.mkdir(parents=True, exist_ok=True)

def convert_filename(input_filename, modality):
    patient_id = input_filename.split('_')[0]
    return f"{patient_id}__{modality}.nii.gz"

def convert_contour_filename(input_filename):
    patient_id = input_filename.split('_')[0]
    return f"{patient_id}__TumorContour.npy"

def copy_and_rename(input_path, output_path, modality):
    for file in input_path.glob("*.nii"):
        new_name = convert_filename(file.name, modality)
        shutil.copy(file, output_path / new_name)

def copy_and_rename_contours(input_path, output_path):
    for file in input_path.glob("*pre*.npy"):
        new_name = convert_contour_filename(file.name)
        shutil.copy(file, output_path / new_name)

copy_and_rename(path_input_pet, path_output_images, "PT")
copy_and_rename(path_input_t1, path_output_images, "T1")
copy_and_rename(path_input_adc, path_output_images, "ADC")
copy_and_rename(path_input_vp, path_output_images, "VP")

copy_and_rename_contours(path_input_contour, path_output_labels)

print("Files have been successfully copied and renamed.")
