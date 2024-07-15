import os
import shutil

# Define the base path
base_path = '/RadOnc-MRI1/Student_Folder/tangzx/Data/HN2013_062_T1_Vp_ADC_FDG'
output_path = '/RadOnc-MRI1/Student_Folder/tangzx/Data/private_data_head_neck/segmentation_txt'

# Create the output directory if it doesn't exist
os.makedirs(output_path, exist_ok=True)

# List of patients without the target file
missing_files = []

# Iterate over each patient folder
for patient_folder in os.listdir(base_path):
    patient_path = os.path.join(base_path, patient_folder)
    
    # Check if it's a directory
    if os.path.isdir(patient_path):
        patient_id = patient_folder[:4]  # First 4 characters of the folder name

        # Check the preRT and 2wkRT folders
        for subfolder in ['preRT', '2wkRT']:
            subfolder_path = os.path.join(patient_path, subfolder)
            
            if os.path.exists(subfolder_path):
                found_prim_file = False
                txt_files = [f for f in os.listdir(subfolder_path) if f.endswith('.txt')]

                # Iterate over .txt files in the subfolder
                for file in txt_files:
                    if 'prim' in file:
                        found_prim_file = True
                        # Construct the new filename
                        prefix = 'pre' if subfolder == 'preRT' else 'post'
                        new_filename = f"{patient_id}_{prefix}_prim.txt"
                        source_file = os.path.join(subfolder_path, file)
                        destination_file = os.path.join(output_path, new_filename)

                        # Copy the file to the new location with the new name
                        shutil.copy(source_file, destination_file)
                
                # If no 'prim' file was found but there's exactly one .txt file, treat it as a 'prim' file
                if not found_prim_file and len(txt_files) == 1:
                    file = txt_files[0]
                    prefix = 'pre' if subfolder == 'preRT' else 'post'
                    new_filename = f"{patient_id}_{prefix}_prim.txt"
                    source_file = os.path.join(subfolder_path, file)
                    destination_file = os.path.join(output_path, new_filename)

                    # Copy the file to the new location with the new name
                    shutil.copy(source_file, destination_file)
                elif not found_prim_file:
                    missing_files.append(f"{patient_folder} - {subfolder}")

# Print patients without the target file
if missing_files:
    print("Patients without the target 'prim' file:")
    for missing in missing_files:
        print(missing)
else:
    print("All target files were found and copied successfully.")
