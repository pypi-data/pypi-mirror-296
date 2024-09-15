import pytest
import os
import geopandas
import tempfile
from SuomiGeoData import Paituli


@pytest.fixture(scope='class')
def class_instance():

    yield Paituli()


def test_save_indexmap_tdb(
    class_instance
):
    # pass test
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_file = os.path.join(tmp_dir, "indexmap_tdb.shp")
        result = class_instance.save_indexmap_tdb(tmp_file)
        assert os.path.exists(tmp_file) is True
        assert isinstance(geopandas.read_file(tmp_file), geopandas.GeoDataFrame) is True
        assert result is True

    assert os.path.exists(tmp_file) is False

    # error test
    with pytest.raises(Exception) as exc_info:
        class_instance.save_indexmap_tdb('invalid_file_extension.sh')
    assert exc_info.value.args[0] == 'Could not OGR format driver from the file path.'


def test_is_valid_label_tdb(
    class_instance
):

    # pass test
    assert class_instance.is_valid_label_tdb('K2344R') is True
    assert class_instance.is_valid_label_tdb('invalid_label') is False
