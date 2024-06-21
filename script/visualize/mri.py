import nibabel as nib
import matplotlib.pyplot as plt

def load_nifti_file(nifti_path):
    # Load the nii file
    nifti_img = nib.load(nifti_path)
    nifti_data = nifti_img.get_fdata()
    return nifti_data

def display_slices(nifti_data):
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    slice_0 = nifti_data[nifti_data.shape[0] // 2, :, :]
    slice_1 = nifti_data[:, nifti_data.shape[1] // 2, :]
    slice_2 = nifti_data[:, :, nifti_data.shape[2] // 2]

    axes[0].imshow(slice_0.T, cmap="gray", origin="lower")
    axes[0].set_title('Sagittal Slice')

    axes[1].imshow(slice_1.T, cmap="gray", origin="lower")
    axes[1].set_title('Coronal Slice')

    axes[2].imshow(slice_2.T, cmap="gray", origin="lower")
    axes[2].set_title('Axial Slice')

    plt.show()

nifti_path = '/RadOnc-MRI1/Student_Folder/tangzx/Data/private_data_head_neck/mri_post_t1/UM01_post_mri_t1.nii'
nifti_data = load_nifti_file(nifti_path)
display_slices(nifti_data)
