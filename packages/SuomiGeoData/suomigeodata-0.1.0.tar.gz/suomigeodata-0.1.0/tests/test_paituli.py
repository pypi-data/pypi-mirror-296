import pytest
import os
import geopandas
import tempfile
from SuomiGeoData import Paituli


@pytest.fixture(scope='class')
def class_instance():

    yield Paituli()


def test_save_indexmap(
    class_instance
):
    # pass test for saving index map
    with tempfile.TemporaryDirectory() as tmp_dir:
        # DEM
        dem_file = os.path.join(tmp_dir, "indexmap_dem.shp")
        save_dem = class_instance.save_indexmap_dem(dem_file)
        assert save_dem is True
        dem_gdf = geopandas.read_file(dem_file)
        assert isinstance(dem_gdf, geopandas.GeoDataFrame) is True
        assert dem_gdf.shape[0] == 10320
        # topographical database
        tdb_file = os.path.join(tmp_dir, "indexmap_tdb.shp")
        save_tdb = class_instance.save_indexmap_tdb(tdb_file)
        assert save_tdb is True
        tdb_gdf = geopandas.read_file(tdb_file)
        assert isinstance(tdb_gdf, geopandas.GeoDataFrame) is True
        assert tdb_gdf.shape[0] == 3132

    assert os.path.exists(tmp_dir) is False

    # error test of saving DEM index map
    with pytest.raises(Exception) as exc_info:
        class_instance.save_indexmap_dem('invalid_file_extension.sh')
    assert exc_info.value.args[0] == 'Could not OGR format driver from the file path.'

    # error test of saving topographical database index map
    with pytest.raises(Exception) as exc_info:
        class_instance.save_indexmap_tdb('invalid_file_extension.sh')
    assert exc_info.value.args[0] == 'Could not OGR format driver from the file path.'


def test_is_valid_label(
    class_instance
):

    # pass test for DEM
    assert class_instance.is_valid_label_dem('K3244G') is True
    assert class_instance.is_valid_label_dem('invalid_label') is False

    # pass test for topographical database
    assert class_instance.is_valid_label_tdb('K2344R') is True
    assert class_instance.is_valid_label_tdb('invalid_label') is False


def test_download_by_labels(
    class_instance
):

    # test for downloading DEM
    with tempfile.TemporaryDirectory() as dem_dir:
        # download test
        class_instance.dem_download_by_labels(['X4344A'], dem_dir) is True
        # download test with customized HTTP headers
        class_instance.dem_download_by_labels(['X4344A'], dem_dir, http_headers={'Host': 'www.nic.funet.fi'}) is True
        # error test for invalid label
        with pytest.raises(Exception) as exc_info:
            class_instance.dem_download_by_labels(['ABCDE'], dem_dir)
        assert exc_info.value.args[0] == 'The label "ABCDE" does not exist in the index map.'
    # errot test for invalid directory
    with pytest.raises(Exception) as exc_info:
        class_instance.dem_download_by_labels(['X4344A'], dem_dir)
    assert exc_info.value.args[0] == f'The folder path "{dem_dir}" is not a valid directory.'

    # test for downloading topographical database
    with tempfile.TemporaryDirectory() as tdb_dir:
        # download test
        class_instance.tdb_download_by_labels(['J3224R'], tdb_dir) is True
        # download test with customized HTTP headers
        class_instance.tdb_download_by_labels(['J3224R'], tdb_dir, http_headers={'Host': 'www.nic.funet.fi'}) is True
        # error test for invalid label
        with pytest.raises(Exception) as exc_info:
            class_instance.tdb_download_by_labels(['ABCDE'], tdb_dir)
        assert exc_info.value.args[0] == 'The label "ABCDE" does not exist in the index map.'
    # errot test for invalid directory
    with pytest.raises(Exception) as exc_info:
        class_instance.tdb_download_by_labels(['J3224R'], tdb_dir)
    assert exc_info.value.args[0] == f'The folder path "{tdb_dir}" is not a valid directory.'
