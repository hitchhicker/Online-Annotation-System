from online_annotation_system.models import BoundingBox, Object, Size
from online_annotation_system.xml_generater import XMLGenerator
import xml.etree.cElementTree as ET
import pytest


def test_xml_build(mocked_xml_generator):
    mocked_xml_generator.build_xml_tree()
    assert ET.tostring(
        mocked_xml_generator.root) == b'<annotation>\n  <folder>glass</folder>\n  <filename>test.jpg</filename>\n  <path>test_path</path>\n  <source>\n    <database>BingBin</database>\n  </source>\n  <size>\n    <width>240</width>\n    <height>280</height>\n    <depth>3</depth>\n  </size>\n  <segmented>0</segmented>\n  <object>\n    <name>glass</name>\n    <pose>Unspecified</pose>\n    <truncated>0</truncated>\n    <difficult>0</difficult>\n    <bndbox>\n      <xmin>48.0</xmin>\n      <ymin>144.0</ymin>\n      <xmax>168.0</xmax>\n      <ymax>336.0</ymax>\n    </bndbox>\n  </object>\n</annotation>\n'


@pytest.fixture
def mocked_bounding_box():
    annotation = BoundingBox(relative_x=0.2,
                             relative_y=0.3,
                             relative_width=0.5,
                             relative_height=0.4,
                             img_height=480,
                             img_width=240)
    return annotation


def test_bounding_box_init(mocked_bounding_box):
    assert mocked_bounding_box.x_min == 48
    assert mocked_bounding_box.y_min == 144
    assert mocked_bounding_box.x_max == 168
    assert mocked_bounding_box.y_max == 336


@pytest.fixture
def mocked_object(mocked_bounding_box):
    object = Object(name='glass', bounding_box=mocked_bounding_box)
    return object


@pytest.fixture
def mocked_size():
    size = Size(width=240, height=280, depth=3)
    return size


@pytest.fixture
def mocked_xml_generator(mocked_size, mocked_object):
    mocked_xml_generator = XMLGenerator(folder='glass',
                                        filename='test.jpg',
                                        path='test_path',
                                        size=mocked_size,
                                        objects=[mocked_object])
    return mocked_xml_generator


def test_get_xml_file_name(mocked_xml_generator):
    assert mocked_xml_generator.xml_file_name == 'test.xml'
