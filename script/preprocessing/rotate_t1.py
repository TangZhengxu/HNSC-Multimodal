import SimpleITK as sitk
import numpy as np
import os

def load_nii(file_path):
    # Load the .nii file
    image = sitk.ReadImage(file_path)
    # Check if the direction is orthonormal
    direction = image.GetDirection()
    if not np.allclose(np.dot(direction, np.transpose(direction)), np.eye(len(direction)), atol=1e-5):
        print(f"Non-orthonormal direction cosines detected in {file_path}. Resetting to identity matrix.")
        image.SetDirection(np.eye(image.GetDimension()).flatten())
    return image

def save_nii(image, file_path):
    # Save the image to a .nii file
    sitk.WriteImage(image, file_path)

def process_data(image):
    data = sitk.GetArrayFromImage(image)

    # rotate 90 degrees counterclockwise and then flip along the y-axis
    data_rotated = np.rot90(data, k=1, axes=(1, 2))
    data_flipped = np.flip(data_rotated, axis=1)

    # Convert the numpy array back 
    processed_image = sitk.GetImageFromArray(data_flipped)

    # Copy the original image metadata (spacing, origin, direction) to the processed image
    processed_image.SetSpacing(image.GetSpacing())
    processed_image.SetOrigin(image.GetOrigin())
    processed_image.SetDirection(image.GetDirection())

    return processed_image

def process_all_files(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith(".nii"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)

            try:
                # Load the input image
                input_image = load_nii(input_path)

                # Process the data
                processed_image = process_data(input_image)

                # Save the processed image
                save_nii(processed_image, output_path)

                print(f"Processed {filename} and saved to {output_path}")
            except Exception as e:
                print(f"Failed to process {filename}: {e}")

# Example usage
input_directory = '/RadOnc-MRI1/Student_Folder/tangzx/Data/resample/pre_t1_incorrect_direction'  
output_directory = '/RadOnc-MRI1/Student_Folder/tangzx/Data/resample/pre_t1_rotate'  
process_all_files(input_directory, output_directory)
