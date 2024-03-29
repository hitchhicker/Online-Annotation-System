import pytest

from online_annotation_system.models import Annotations


@pytest.fixture
def mocked_annotations():
    return [{
        'src': 'blob:http://localhost:5000/69d40be8-25f1-43d1-8440-e623d2d40bde',
        'shapes': [{
            'style': {},
            'geometry': {
                'width': 0.392,
                'height': 0.45645645645645644,
                'x': 0.52,
                'y': 0.2132132132132132},
            'type': 'rect'
        }],
        'context': 'http://localhost:5000/',
        'text': 'glass'},
        {
            'src': 'blob:http://localhost:5000/69d40be8-25f1-43d1-8440-e623d2d40bde',
            'shapes': [{
                'style': {},
                'geometry': {
                    'width': 0.392,
                    'height': 0.45645645645645644,
                    'x': 0.52,
                    'y': 0.2132132132132132},
                'type': 'rect'
            }],
            'context': 'http://localhost:5000/',
            'text': 'paper'}
    ]


def test_iter_annotations(mocked_annotations):
    annotations = list(Annotations(mocked_annotations, image_width=500, image_height=343))
    label1, bounding_box = annotations[0]
    label2, _ = annotations[1]
    assert label1 == 'glass'
    assert bounding_box.x_min == 260.0
    assert bounding_box.x_max == 456.0
    assert bounding_box.y_min == 73.13213213213213
    assert bounding_box.y_max == 229.69669669669668
    assert label2 == 'paper'
