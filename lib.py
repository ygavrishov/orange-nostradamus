import cv2
import xml.etree.ElementTree as ET
from lxml import etree
import matplotlib.pyplot as plt
import os

def save_annotated_image(image_file, image_element, result_file_name):
    # Load the image using OpenCV
    image = cv2.imread(image_file)
    
    # Draw bounding boxes on the image
    for box in image_element.findall('box'):
        label = get_label_name(box)
        
        xtl = float(box.get('xtl'))
        ytl = float(box.get('ytl'))
        xbr = float(box.get('xbr'))
        ybr = float(box.get('ybr'))
    
        cv2.rectangle(image, (int(xtl), int(ytl)), (int(xbr), int(ybr)), (0, 255, 0), 2)
    
        cv2.putText(image, label, (int(xtl), int(ytl) - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        #print(label)
    
    cv2.imwrite(result_file_name, image)
    return image

def get_annotated_image_element(xml_file, image_file):
    # Parse the XML file
    parser = etree.XMLParser(encoding='utf-8')
    tree = etree.parse(xml_file, parser)
    root = tree.getroot()
    
    # Get image name from the file path (assuming the file name matches the name in the XML)
    image_name = image_file.split('/')[-2] + '/' + image_file.split('/')[-1]
    
    # Find the image element in the XML
    image_element = None
    for img in root.findall('image'):
        if img.get('name') == image_name:
            image_element = img
            break
    return image_element
    
def draw_image(image):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.figure(figsize=(10,10))
    plt.imshow(image_rgb)
    plt.show()

def get_label_name(box):
    label = box.get('label')
    if label == 'Текст':
        label = 'Text'
    if label == 'Шкаф':
        label = 'Cabinet'
    p = None
    for attribute in box.findall('attribute'):
        if attribute.get('name') == 'Полюсность':
            p = attribute.text
    if p != None:
        label += '-' + p
    return label

def get_all_labels(folder):
    annotation_files = []
    labels = set()
    
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.xml'):
                annotation_files.append(os.path.join(root, file))
    
    parser = etree.XMLParser(encoding='utf-8')
    for xml_file in annotation_files:
        tree = etree.parse(xml_file, parser)
        root = tree.getroot()
        for image_element in root.findall('image'):
            for box in image_element.findall('box'):
                label = get_label_name(box)
                labels.add(label)
    return labels