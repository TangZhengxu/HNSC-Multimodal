import numpy as np
import nibabel as nib
import os

def npy_to_nii(npy_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(npy_folder):
        if filename.endswith('.npy'):
            # Load the npy file
            npy_path = os.path.join(npy_folder, filename)
            data = np.load(npy_path)
            
            # Convert the numpy array data type to int16
            data = data.astype(np.int16)  
            
            # Convert the numpy array to a nii
            nii_image = nib.Nifti1Image(data, np.eye(4))
            
            # Save the nii as a .nii.gz file
            output_filename = os.path.splitext(filename)[0] + '.nii.gz'
            output_path = os.path.join(output_folder, output_filename)
            nib.save(nii_image, output_path)
            print(f'Converted {npy_path} to {output_path}')

npy_folder = '/RadOnc-MRI1/Student_Folder/tangzx/Data/private_data_head_neck/labelsTr'
output_folder = '/RadOnc-MRI1/Student_Folder/tangzx/Data/private_data_head_neck/labelsTr_nii'
npy_to_nii(npy_folder, output_folder)
