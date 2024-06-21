import os
import nibabel as nib

# base path and output path
base_path = '/RadOnc-MRI1/Student_Folder/tangzx/Data/HN2013_062_T1_Vp_ADC_FDG'
output_folder = '/RadOnc-MRI1/Student_Folder/tangzx/Data/private_data_head_neck/mri_post_adc'

os.makedirs(output_folder, exist_ok=True)

def convert_analyze_to_nifti(hdr_path, img_path, output_filename):
    # Load the adc image
    analyze_img = nib.AnalyzeImage.from_filename(hdr_path)
    
    # Convert to nii format
    nifti_img = nib.Nifti1Image(analyze_img.get_fdata(), analyze_img.affine)
    
    # Save the nii image
    nifti_output_path = os.path.join(output_folder, output_filename)
    nib.save(nifti_img, nifti_output_path)
    print(f'Successfully converted to NIfTI and saved to: {nifti_output_path}')

#looping
for patient_folder in os.listdir(base_path):
    patient_path = os.path.join(base_path, patient_folder)
    
    if os.path.isdir(patient_path):
        preRT_path = os.path.join(patient_path, '2wkRT')
        
        if os.path.isdir(preRT_path):
            hdr_filename = 'MADC_2wkRT.hdr'
            img_filename = 'MADC_2wkRT.img'
            
            hdr_path = os.path.join(preRT_path, hdr_filename)
            img_path = os.path.join(preRT_path, img_filename)
            
            if os.path.exists(hdr_path) and os.path.exists(img_path):
                patient_id = patient_folder[:4]
                
                output_filename = f'{patient_id}_post_adc.nii'
                
                convert_analyze_to_nifti(hdr_path, img_path, output_filename)
