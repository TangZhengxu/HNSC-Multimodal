import os
import pandas as pd
import numpy as np

def load_roi_mask(voi_path, save_path, image_size_dict):
    '''
    :param voi_path: path of txt format voi
    :param save_path: file path to save voi in numpy format
    :param image_size_dict: dictionary with patient names as keys and (x_dim, y_dim, z_dim) as values
    :return: numpy array, mask of shape (z_dim, x_dim, y_dim)
    '''
    patient_prefix = os.path.basename(voi_path)[:4]
    if patient_prefix not in image_size_dict:
        print(f"Image size not found for patient with prefix {patient_prefix}")
        return

    x_dim, y_dim, z_dim = image_size_dict[patient_prefix]

    input_data = pd.read_csv(voi_path, sep=' ', header=None)  # read the input data from the txt file
    input_data = input_data.values  # convert the dataframe to numpy array

    mask = np.zeros((z_dim, x_dim, y_dim))  # create a zero mask of shape (z_dim, x_dim, y_dim)

    file_out_of_bounds = False

    for i in range(input_data.shape[0]):  # loop through each entry in the input data
        try:
            z_index = int(input_data[i][0].split('_')[1]) - 1
            x_index = int(input_data[i][0].split('_')[4])
            y_index = int(input_data[i][0].split('_')[3])

            if x_index >= x_dim or y_index >= y_dim:
                file_out_of_bounds = True

            if 0 <= z_index < z_dim and 0 <= x_index < x_dim and 0 <= y_index < y_dim:
                mask[z_index, x_index, y_index] = 1

        except IndexError as e:
            print(f"IndexError at row {i}: {e}")
        except Exception as e:
            print(f"Error at row {i}: {e}")

    if file_out_of_bounds:
        print(f"File {os.path.basename(voi_path)} has indices out of bounds.")

    np.save(save_path, mask.astype(bool))  # save the mask as a numpy array in boolean format
    return mask  # return the mask array

def process_all_files(input_dir, output_dir, image_size_dict):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            voi_path = os.path.join(input_dir, filename)
            save_path = os.path.join(output_dir, filename.replace('.txt', '.npy'))
            load_roi_mask(voi_path, save_path, image_size_dict)
            print(f"Processed {filename} and saved to {save_path}")

input_directory = '/RadOnc-MRI1/Student_Folder/tangzx/Data/private_data_head_neck/segmentation_pre/'  # replace with your input folder path
output_directory = '/RadOnc-MRI1/Student_Folder/tangzx/Data/private_data_head_neck/contour_pre/'  # replace with your output folder path

# read the image sizes and voxel sizes from csv file
df = pd.read_csv('/RadOnc-MRI1/Student_Folder/tangzx/Data/private_data_head_neck/image_size.csv')  # 请替换为包含图像大小信息的csv文件路径
image_size_dict = df.set_index(df['Patient'].str[:4])['Image Size'].to_dict()
image_size_dict = {k: tuple(map(int, v.strip('()').replace(' ', '').split(',')))[:3] for k, v in image_size_dict.items()}

process_all_files(input_directory, output_directory, image_size_dict)
