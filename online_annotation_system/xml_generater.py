import os
import logging
import xml.etree.cElementTree as ET

logger = logging.getLogger("xml_generator")


class XMLGenerator:
    def __init__(self, folder, filename, path, size, objects):
        self.size = size
        self.path = path
        self.filename = filename
        self.folder = folder
        self.objects = objects
        self.database = 'BingBin'
        self.segmented = 0
        self.root = None

    @staticmethod
    def indent(elem, level=0):
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                XMLGenerator.indent(elem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    @property
    def xml_file_name(self):
        return os.path.splitext(self.filename)[0] + '.xml'

    def build_xml_tree(self):
        logger.info("Start building xml tree.")
        self.root = ET.Element("annotation")

        folder = ET.SubElement(self.root, "folder")
        folder.text = self.folder

        filename = ET.SubElement(self.root, "filename")
        filename.text = self.filename

        path = ET.SubElement(self.root, "path")
        path.text = self.path

        source = ET.SubElement(self.root, "source")

        database = ET.SubElement(source, "database")
        database.text = self.database

        size = ET.SubElement(self.root, "size")
        width = ET.SubElement(size, "width")
        width.text = str(self.size.width)
        height = ET.SubElement(size, "height")
        height.text = str(self.size.height)
        depth = ET.SubElement(size, "depth")
        depth.text = str(self.size.depth)

        segmented = ET.SubElement(self.root, "segmented")
        segmented.text = str(self.segmented)

        for obj in self.objects:
            obj_ = ET.SubElement(self.root, "object")
            name = ET.SubElement(obj_, "name")
            name.text = obj.name
            pose = ET.SubElement(obj_, "pose")
            pose.text = obj.pose
            truncated = ET.SubElement(obj_, "truncated")
            truncated.text = str(obj.truncated)
            difficult = ET.SubElement(obj_, "difficult")
            difficult.text = str(obj.difficult)
            bndbox = ET.SubElement(obj_, "bndbox")
            xmin = ET.SubElement(bndbox, "xmin")
            xmin.text = str(obj.bounding_box.x_min)
            ymin = ET.SubElement(bndbox, "ymin")
            ymin.text = str(obj.bounding_box.y_min)
            xmax = ET.SubElement(bndbox, "xmax")
            xmax.text = str(obj.bounding_box.x_max)
            ymax = ET.SubElement(bndbox, "ymax")
            ymax.text = str(obj.bounding_box.y_max)

        self.indent(self.root)
        logger.info("Finish building xml tree.")

    def write_xml_to_path(self, base_path):
        if self.root is not None:
            tree = ET.ElementTree(self.root)
            where_to_store = os.path.join(base_path, self.folder)
            logger.info("Write " + str(self.xml_file_name) + " to " + str(where_to_store))
            if not os.path.exists(where_to_store):
                os.mkdir(where_to_store)
            tree.write(os.path.join(where_to_store, self.xml_file_name), xml_declaration=True, encoding='utf-8',
                       method="xml")
