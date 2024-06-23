import numpy as np
import matplotlib.pyplot as plt

def visualize_npy(file_path):
    data = np.load(file_path)

    print(f"Shape of the data: {data.shape}")
    
    x_dim, y_dim, z_dim = data.shape

    print(f"X dimension size: {x_dim}")
    print(f"Y dimension size: {y_dim}")
    print(f"Z dimension size: {z_dim}")

    fig, axes = plt.subplots(1, 5, figsize=(15, 5))
    for i in range(5):
        slice_idx = i * 10
        axes[i].imshow(data[:, :, slice_idx], cmap='gray')
        axes[i].set_title(f'Slice {slice_idx}')
        axes[i].axis('off')
    
    plt.show()

npy_file_path = '/RadOnc-MRI1/Student_Folder/tangzx/Data/private_data_head_neck/numpy_files_4/UM46_pre_prim.npy'  # Replace with your actual npy file path
visualize_npy(npy_file_path)
