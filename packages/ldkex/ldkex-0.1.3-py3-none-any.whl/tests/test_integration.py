import os

import pytest

from ldkex import Extractor


@pytest.fixture
def setup_extractor():
    extractor = Extractor()
    return extractor


@pytest.mark.parametrize("file_path, "
                         "expected_geometries, "
                         "expected_geometries_no_duplicates, "
                         "expected_points, "
                         "expected_lines, "
                         "expected_polygons, "
                         "expected_points_no_duplicates, "
                         "expected_lines_no_duplicates, "
                         "expected_polygons_no_duplicates", [
                             ('test_data-01.ldk', 242830, 23001, 234713, 6183, 1934, 20859, 1798, 344),
                             ('test_data-02.ldk', 30932, 28196, 28258, 2368, 306, 25696, 2194, 306),
                             ('test_data-03.trk', 1, 1, 0, 1, 0, 0, 1, 0),
                         ])
def test_extract_file(setup_extractor, file_path, expected_geometries, expected_geometries_no_duplicates,
                      expected_points, expected_lines, expected_polygons, expected_points_no_duplicates,
                      expected_lines_no_duplicates, expected_polygons_no_duplicates):

    test_dir = os.path.dirname(__file__)
    full_file_path = os.path.join(test_dir, 'data', file_path)

    extractor = setup_extractor
    with open(full_file_path, 'rb') as file:
        extractor.extract(file)

    assert len(extractor.geometries) == expected_geometries
    assert len(extractor.get_points()) == expected_points
    assert len(extractor.get_lines()) == expected_lines
    assert len(extractor.get_polygons()) == expected_polygons

    extractor.geometries.remove_duplicates(fields=['name', 'coordinates', 'outline_color'])
    assert len(extractor.geometries) == expected_geometries_no_duplicates
    assert len(extractor.get_points()) == expected_points_no_duplicates
    assert len(extractor.get_lines()) == expected_lines_no_duplicates
    assert len(extractor.get_polygons()) == expected_polygons_no_duplicates
