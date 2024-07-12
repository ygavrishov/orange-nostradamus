import xml.etree.ElementTree as ET
import os
from lib import get_all_labels, get_label_name

def convert_cvat_to_yolo(xml_file, output_dir, labels):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    for image in root.findall('image'):
        image_id = image.get('id')
        file_name = image.get('name')
        width = int(image.get('width'))
        height = int(image.get('height'))

        yolo_annotations = []

        for box in image.findall('box'):
            label = get_label_name(box)
            xtl = float(box.get('xtl'))
            ytl = float(box.get('ytl'))
            xbr = float(box.get('xbr'))
            ybr = float(box.get('ybr'))

            # Calculate YOLO format values
            x_center = (xtl + xbr) / 2.0 / width
            y_center = (ytl + ybr) / 2.0 / height
            bbox_width = (xbr - xtl) / width
            bbox_height = (ybr - ytl) / height

            # Create a YOLO annotation string
            l_index = labels.index(label)
            yolo_annotations.append(f"{l_index} {x_center} {y_center} {bbox_width} {bbox_height}")

        # Write YOLO annotations to a file
        base_name = os.path.splitext(os.path.basename(file_name))[0]
        yolo_file_path = os.path.join(output_dir, f"{base_name}.txt")
        with open(yolo_file_path, 'w') as yolo_file:
            yolo_file.write("\n".join(yolo_annotations))

        print(f"Converted {file_name} to {yolo_file_path}")

root_folder = r'c:\DevProjects\Contests\ekf-2024\dataset\flatten'
xml_file = root_folder + r'\annotations-330.xml'
output_dir = root_folder + r'\yolo'
image_dir = root_folder + r'\images'

labels = list(get_all_labels(root_folder))

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

convert_cvat_to_yolo(xml_file, output_dir, labels)
print (labels)