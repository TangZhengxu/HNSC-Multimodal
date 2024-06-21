import os
import numpy as np
import pydicom
import nibabel as nib

def load_dicom_series(dicom_dir):
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

    pixel_spacing = ref_ds.PixelSpacing
    slice_thickness = ref_ds.SliceThickness

    slice_positions = [pydicom.dcmread(f).ImagePositionPatient[2] for f in dicom_files]
    slice_positions = np.array(slice_positions)
    slice_positions.sort()
    slice_thickness = np.mean(np.diff(slice_positions))

    orientation = ref_ds.ImageOrientationPatient
    position = ref_ds.ImagePositionPatient

    affine = np.eye(4)
    affine[0, :3] = np.array(orientation[:3]) * pixel_spacing[0]
    affine[1, :3] = np.array(orientation[3:]) * pixel_spacing[1]
    affine[2, 2] = slice_thickness
    affine[:3, 3] = position

    return image, affine

def dicom_to_nifti(dicom_dir, output_file):
    image, affine = load_dicom_series(dicom_dir)

    if image is None or affine is None:
        print(f"No DICOM files found in {dicom_dir}")
        return

    nifti_img = nib.Nifti1Image(image, affine)

    nib.save(nifti_img, output_file)

def process_all_patients(data_root, target_folder):

    os.makedirs(target_folder, exist_ok=True)

    for patient_folder in os.listdir(data_root):
        patient_path = os.path.join(data_root, patient_folder)
        if not os.path.isdir(patient_path):
            continue

        pre_rt_folder = os.path.join(patient_path, 'preRT')

        patient_id = patient_folder[:4]
        output_nifti_file = os.path.join(target_folder, f'{patient_id}_pre_mri_t1.nii')

        dicom_to_nifti(pre_rt_folder, output_nifti_file)


data_root = '/RadOnc-MRI1/Student_Folder/tangzx/Data/HN2013_062_T1_Vp_ADC_FDG/'
target_folder = '/RadOnc-MRI1/Student_Folder/tangzx/Data/private_data_head_neck/mri_pre_t1_new_new'
process_all_patients(data_root, target_folder)
