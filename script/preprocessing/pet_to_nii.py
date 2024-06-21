import os
import nibabel as nib
import numpy as np

def fix_header_zoom(analyze_img):
    header = analyze_img.header
    zooms = header.get_zooms()
    if np.any(np.array(zooms) <= 0):
        print("Fixing zoom values in header")
        fixed_zooms = tuple(max(1, zoom) for zoom in zooms)
        header.set_zooms(fixed_zooms)
    return analyze_img

def convert_pet_to_nifti(patient_folder, target_folder):
    preRT_folder = os.path.join(patient_folder, 'preRT')
    pet_hdr = os.path.join(preRT_folder, 'MPET_SUV_preRT.hdr')
    pet_img = os.path.join(preRT_folder, 'MPET_SUV_preRT.img')

    # Check if both hdr and img files exist
    if not (os.path.exists(pet_hdr) and os.path.exists(pet_img)):
        print(f"No PET file found for patient: {os.path.basename(patient_folder)}")
        return

    try:
        # Load the pet format image
        analyze_img = nib.AnalyzeImage.from_filename(pet_hdr)

        analyze_img = fix_header_zoom(analyze_img)

        patient_name = os.path.basename(patient_folder)
        output_filename = f"{patient_name[:4]}_pre_pet.nii"
        output_path = os.path.join(target_folder, output_filename)

        # Save the nii as a NIfTI file
        nib.save(analyze_img, output_path)
        print(f"Converted {pet_hdr} and {pet_img} to {output_path}")
    except Exception as e:
        print(f"Failed to convert {patient_folder} due to error: {e}")

def process_all_patients(data_folder, target_folder):
    os.makedirs(target_folder, exist_ok=True)

    patient_folders = [os.path.join(data_folder, d) for d in os.listdir(data_folder) if os.path.isdir(os.path.join(data_folder, d))]

    for patient_folder in patient_folders:
        convert_pet_to_nifti(patient_folder, target_folder)

# paths
data_folder = '/RadOnc-MRI1/Student_Folder/tangzx/Data/HN2013_062_T1_Vp_ADC_FDG/'
target_folder = '/RadOnc-MRI1/Student_Folder/tangzx/Data/private_data_head_neck/pet_pre/'

process_all_patients(data_folder, target_folder)
