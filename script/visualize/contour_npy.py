import numpy as np
import matplotlib.pyplot as plt
import os

def visualize_npy_file(npy_path):
    mask = np.load(npy_path)
    

    z_dim, x_dim, y_dim = mask.shape

    start_slice = 20
    end_slice = 38

    fig, axes = plt.subplots(nrows=1, ncols=end_slice - start_slice, figsize=(20, 10))
    
    for i, ax in enumerate(axes):
        slice_index = start_slice + i
        ax.imshow(mask[slice_index, :, :], cmap='gray')
        ax.set_title(f'Slice {slice_index}')
        ax.axis('off')
    
    plt.show()

npy_file_path = '/RadOnc-MRI1/Student_Folder/tangzx/Data/private_data_head_neck/contour_pre/VA11_pre_prim.npy' # Replace with your .npy file path
visualize_npy_file(npy_file_path)
