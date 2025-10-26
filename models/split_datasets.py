import os
import shutil
import random

def split_dataset(image_dir, label_dir, output_dir, train_ratio=0.8):
    """
    Splits the dataset into training and validation sets.

    Args:
        image_dir (str): Path to the directory containing images.
        label_dir (str): Path to the directory containing YOLO labels.
        output_dir (str): Path to the directory where the split dataset will be saved.
        train_ratio (float): The proportion of the dataset to be used for training.
    """
    train_images_path = os.path.join(output_dir, 'train', 'images')
    train_labels_path = os.path.join(output_dir, 'train', 'labels')
    val_images_path = os.path.join(output_dir, 'val', 'images')
    val_labels_path = os.path.join(output_dir, 'val', 'labels')

    os.makedirs(train_images_path, exist_ok=True)
    os.makedirs(train_labels_path, exist_ok=True)
    os.makedirs(val_images_path, exist_ok=True)
    os.makedirs(val_labels_path, exist_ok=True)

    image_files = [os.path.splitext(f)[0] for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))]

    random.shuffle(image_files)

    split_index = int(len(image_files) * train_ratio)

    train_files = image_files[:split_index]
    val_files = image_files[split_index:]

    print(f"Total files: {len(image_files)}")
    print(f"Training files: {len(train_files)}")
    print(f"Validation files: {len(val_files)}")

    def copy_files(file_list, source_image_dir, source_label_dir, dest_image_dir, dest_label_dir):
        for filename_no_ext in file_list:
    
            image_extension = ''
            for ext in ['.jpg', '.jpeg', '.png', '.PNG']:
                if os.path.exists(os.path.join(source_image_dir, filename_no_ext + ext)):
                    image_extension = ext
                    break
            
            if not image_extension:
                print(f"Warning: Could not find image for {filename_no_ext}")
                continue

            src_image = os.path.join(source_image_dir, filename_no_ext + image_extension)
            src_label = os.path.join(source_label_dir, filename_no_ext + '.txt')
            
            dest_image = os.path.join(dest_image_dir, filename_no_ext + image_extension)
            dest_label = os.path.join(dest_label_dir, filename_no_ext + '.txt')

            shutil.copy(src_image, dest_image)
            if os.path.exists(src_label):
                shutil.copy(src_label, dest_label)
            else:
                print(f"Warning: Label file not found for {filename_no_ext}")


    print("\nCopying training files...")
    copy_files(train_files, image_dir, label_dir, train_images_path, train_labels_path)

    print("Copying validation files...")
    copy_files(val_files, image_dir, label_dir, val_images_path, val_labels_path)

    print("\nDataset split successfully!")

def main():
    source_images = 'data/kaggle/images/'
    source_labels = 'data/kaggle/labels/'

    output_directory = 'data/kaggle/dataset/'

    training_ratio = 0.8

    split_dataset(source_images, source_labels, output_directory, training_ratio)

if __name__ == '__main__':
    main()