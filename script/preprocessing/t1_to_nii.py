import os
import numpy as np
import pydicom
import nibabel as nib

def load_dicom_series(dicom_dir):
    # Get a list of all DICOM files in the directory
    dicom_files = []
    for root, dirs, files in os.walk(dicom_dir):
        for file in files:
            if file.endswith('.dcm'):
                dicom_files.append(os.path.join(root, file))

    if not dicom_files:
        return None, None

    dicom_files.sort(key=lambda f: int(pydicom.dcmread(f).InstanceNumber))

    ref_ds = pydicom.dcmread(dicom_files[0])
    shape = (int(ref_ds.Rows), int(ref_ds.Columns), len(dicom_files))

    image = np.zeros(shape, dtype=ref_ds.pixel_array.dtype)

    for i, file in enumerate(dicom_files):
        ds = pydicom.dcmread(file)
        image[:, :, i] = ds.pixel_array

    return image, ref_ds

def dicom_to_nifti(dicom_dir, output_file):
    image, ref_ds = load_dicom_series(dicom_dir)

    if image is None or ref_ds is None:
        print(f"No DICOM files found in {dicom_dir}")
        return

    nifti_img = nib.Nifti1Image(image, np.eye(4))

    nib.save(nifti_img, output_file)

def process_all_patients(data_root, target_folder):

    os.makedirs(target_folder, exist_ok=True)

    for patient_folder in os.listdir(data_root):
        patient_path = os.path.join(data_root, patient_folder)
        if not os.path.isdir(patient_path):
            continue

        pre_rt_folder = os.path.join(patient_path, '2wkRT')

        patient_id = patient_folder[:4]
        output_nifti_file = os.path.join(target_folder, f'{patient_id}_post_mri_t1.nii')

        dicom_to_nifti(pre_rt_folder, output_nifti_file)

data_root = '/RadOnc-MRI1/Student_Folder/tangzx/Data/HN2013_062_T1_Vp_ADC_FDG/'
target_folder = '/RadOnc-MRI1/Student_Folder/tangzx/Data/private_data_head_neck/mri_post_t1'
process_all_patients(data_root, target_folder)
