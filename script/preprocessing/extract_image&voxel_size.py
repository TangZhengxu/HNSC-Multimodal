import os
import pandas as pd
import nibabel as nib

def get_patient_data(pet_folder):
    data = []

    for filename in os.listdir(pet_folder):
        if filename.endswith('.nii') or filename.endswith('.nii.gz'):
            file_path = os.path.join(pet_folder, filename)
            image = nib.load(file_path)
            image_data = image.get_fdata()
            header = image.header

            patient_name = os.path.splitext(filename)[0]
            image_size = image_data.shape
            voxel_size = header.get_zooms()

            data.append({
                'Patient': patient_name,
                'Image Size': image_size,
                'Voxel Size': voxel_size
            })

    df = pd.DataFrame(data)
    return df


pet_folder = '/RadOnc-MRI1/Student_Folder/tangzx/Data/private_data_head_neck/pet_pre/'  

df = get_patient_data(pet_folder)
print(df)
