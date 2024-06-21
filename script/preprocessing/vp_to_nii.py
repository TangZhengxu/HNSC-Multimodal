import os
import nibabel as nib

def convert_analyze_to_nifti(hdr_file_path, img_file_path, nii_file_path):
    analyze_img = nib.load(img_file_path)
    
    nib.save(analyze_img, nii_file_path)
    print(f"File saved to {nii_file_path}")

def process_patient_data(patient_folder, target_folder):
    preRT_folder = os.path.join(patient_folder, '2wkRT')
    
    patient_id = os.path.basename(patient_folder)[:4]
    
    files_to_convert = ['MVp_2wkRT']

    for file_base in files_to_convert:
        hdr_file_path = os.path.join(preRT_folder, f'{file_base}.hdr')
        img_file_path = os.path.join(preRT_folder, f'{file_base}.img')

        if os.path.exists(hdr_file_path) and os.path.exists(img_file_path):
            nii_file_path = os.path.join(target_folder, f'{patient_id}_post_vp.nii')
            convert_analyze_to_nifti(hdr_file_path, img_file_path, nii_file_path)

def process_all_patients(data_folder, target_folder):
    for patient_folder in os.listdir(data_folder):
        patient_path = os.path.join(data_folder, patient_folder)
        if os.path.isdir(patient_path):
            print(f"Processing {patient_folder}")
            process_patient_data(patient_path, target_folder)

data_folder = '/RadOnc-MRI1/Student_Folder/tangzx/Data/HN2013_062_T1_Vp_ADC_FDG/'
target_folder = '/RadOnc-MRI1/Student_Folder/tangzx/Data/private_data_head_neck/mri_post_vp'

os.makedirs(target_folder, exist_ok=True)

process_all_patients(data_folder, target_folder)
