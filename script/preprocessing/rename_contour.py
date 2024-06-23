import os


folder_path = '/RadOnc-MRI1/Student_Folder/tangzx/Data/private_data_head_neck/6_23_correct_contour/'


for filename in os.listdir(folder_path):
    if 'pre' in filename:

        new_name = filename.split('_')[0] + '_PT.nii.gz'

        old_file = os.path.join(folder_path, filename)

        new_file = os.path.join(folder_path, new_name)

        os.rename(old_file, new_file)

print("done")
