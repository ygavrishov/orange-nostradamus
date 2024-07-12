import os
import shutil
import random

def split_dataset(images_dir, labels_dir, train_dir, val_dir, train_ratio=0.8):
    # Create directories if they don't exist
    os.makedirs(train_dir + '/images', exist_ok=True)
    os.makedirs(train_dir + '/labels', exist_ok=True)
    os.makedirs(val_dir + '/images', exist_ok=True)
    os.makedirs(val_dir + '/labels', exist_ok=True)

    # Get list of all images
    images = [f for f in os.listdir(images_dir) if os.path.isfile(os.path.join(images_dir, f))]
    random.shuffle(images)

    # Split the dataset
    train_count = int(len(images) * train_ratio)

    train_images = images[:train_count]
    val_images = images[train_count:]

    # Move files to train and val directories
    for image in train_images:
        label = os.path.splitext(image)[0] + '.txt'
        shutil.copy(os.path.join(images_dir, image), os.path.join(train_dir, 'images', image))
        shutil.copy(os.path.join(labels_dir, label), os.path.join(train_dir, 'labels', label))

    for image in val_images:
        label = os.path.splitext(image)[0] + '.txt'
        shutil.copy(os.path.join(images_dir, image), os.path.join(val_dir, 'images', image))
        shutil.copy(os.path.join(labels_dir, label), os.path.join(val_dir, 'labels', label))

    print(f"Dataset split: {len(train_images)} train images, {len(val_images)} validation images")

# Example usage
root_folder = r'c:\DevProjects\Contests\ekf-2024\dataset\flatten'
images_dir = root_folder+r'\images'
labels_dir = root_folder+r'\yolo'
train_dir = root_folder+r'\train'
val_dir = root_folder+r'\val'
split_dataset(images_dir, labels_dir, train_dir, val_dir)
