import os
import xml.etree.ElementTree as ET

def convert_voc_to_yolo(xml_file, classes):
    """
    Converts a PASCAL VOC XML annotation file to a YOLO format text file.

    Args:
        xml_file (str): The path to the PASCAL VOC XML file.
        classes (list): A list of class names.

    Returns:
        str: The YOLO formatted annotation string.
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()

    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    yolo_annotations = []

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        
        # PASCAL VOC to YOLO conversion formula
        # x_center = (xmin + xmax) / 2.0 / w
        # y_center = (ymin + ymax) / 2.0 / h
        # width = (xmax - xmin) / w
        # height = (ymax - ymin) / h
        
        bb = ((b[0] + b[1]) / 2.0 / w, (b[2] + b[3]) / 2.0 / h, (b[1] - b[0]) / w, (b[3] - b[2]) / h)
        yolo_annotations.append(str(cls_id) + " " + " ".join([str(a) for a in bb]))

    return "\n".join(yolo_annotations)

def main():
    classes = ["pool"] 

    labels_dir = 'data/kaggle/labels/'

    if not os.path.exists(labels_dir):
        print(f"Error: The directory '{labels_dir}' does not exist.")
        return

    for filename in os.listdir(labels_dir):
        if filename.endswith('.xml'):
            xml_path = os.path.join(labels_dir, filename)
            
            yolo_data = convert_voc_to_yolo(xml_path, classes)
            
            txt_filename = os.path.splitext(filename)[0] + '.txt'
            txt_path = os.path.join(labels_dir, txt_filename)
            
            with open(txt_path, 'w') as f:
                f.write(yolo_data)
            
            print(f"Converted {filename} to {txt_filename}")

if __name__ == '__main__':
    main()