import os
import re
from lxml import etree
from lib import save_annotated_image

def is_convertible_to_int(s):
    return bool(re.match(r"^-?\d+$", s))
    
folder_name = '/home/jovyan/ds/'
annotated_folder_name = '/home/jovyan/ds/annotated_images/'
image_folders = set()
for root, dirs, files in os.walk(folder_name):
    for dir in dirs:
        if is_convertible_to_int(dir):
            image_folder = folder_name + dir
            image_folders.add(image_folder)
print(image_folders)

parser = etree.XMLParser(encoding='utf-8')
for image_folder in image_folders:
    annotation_file = image_folder + '/annotations.xml'
    tree = etree.parse(annotation_file, parser)
    root = tree.getroot()
    for image_element in root.findall('image'):
        image_file = image_folder + '/images/'+image_element.get('name')
        #print(image_file)
        result_file = annotated_folder_name + os.path.basename(image_element.get('name'))
        result_directory = os.path.dirname(result_file)
        os.makedirs(result_directory, exist_ok=True)
        #result_files.append(result_file)
        #print(result_file)
        save_annotated_image(image_file, image_element, result_file)
