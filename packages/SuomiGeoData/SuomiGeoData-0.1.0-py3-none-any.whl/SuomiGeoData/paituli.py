import os
import io
import zipfile
import geopandas
import requests
import typing
from .core import Core


class Paituli:

    '''
    Executes downloading and extracting data from Paituli
    (https://paituli.csc.fi/download.html).

    Attributes:
    -----------
    index_dem : GeoDataFrame
        A GeoDataFrame containing the DEM index map.

    index_td : GeoDataFrame
        A GeoDataFrame containing the topographic database index map.
    '''

    def __init__(
        self
    ) -> None:

        '''
        Initializes the class by loading the GeoDataFrame of index maps.
        '''

        # DEM index map
        self.indexmap_dem = geopandas.read_file(
            os.path.join(
                os.path.dirname(__file__), 'data', 'nls_dem_index.shp'
            )
        )

        # topograhical database index map
        self.indexmap_tdb = geopandas.read_file(
            os.path.join(
                os.path.dirname(__file__), 'data', 'nls_td_index.shp'
            )
        )

    def save_indexmap_dem(
        self,
        file_path: str,
        **kwargs: typing.Any
    ) -> bool:

        '''
        Saves the GeoDataFrame of the DEM index map to the specified file path.

        Parameters
        ----------
        file_path : str
            File path to save the GeoDataFrame.

        **kwargs : optional
            Additional keyword arguments for the
            :meth:`geopandas.GeoDataFrame.to_file` function.

        Returns
        -------
        bool
            True if the file exists at the specified path, False otherwise.
        '''

        validity = Core().is_valid_write_shape_driver(file_path)
        if validity is True:
            self.indexmap_dem.to_file(
                file_path,
                **kwargs
            )
        else:
            raise Exception(
                'Could not OGR format driver from the file path.'
            )

        output = os.path.exists(file_path)

        return output

    @property
    def dem_labels(
        self
    ) -> list[str]:

        '''
        Returns the list of labels from the DEM index map.
        '''

        output = list(self.indexmap_dem['label'])

        return output

    def is_valid_label_dem(
        self,
        label: str
    ) -> bool:

        '''
        Returns whether the label exists in the DEM index map.

        Parameters
        ----------
        label : str
            Name of the label.

        Returns
        -------
        bool
            True if the label exists, False otherwise.
        '''

        return label in self.dem_labels

    def save_indexmap_tdb(
        self,
        file_path: str,
        **kwargs: typing.Any
    ) -> bool:

        '''
        Saves the GeoDataFrame of the topographic database
        index map to the specified file path.

        Parameters
        ----------
        file_path : str
            File path to save the GeoDataFrame.

        **kwargs : optional
            Additional keyword arguments for the
            :meth:`geopandas.GeoDataFrame.to_file` function.

        Returns
        -------
        bool
            True if the file exists at the specified path, False otherwise.
        '''

        validity = Core().is_valid_write_shape_driver(file_path)
        if validity is True:
            self.indexmap_tdb.to_file(
                file_path,
                **kwargs
            )
        else:
            raise Exception(
                'Could not OGR format driver from the file path.'
            )

        output = os.path.exists(file_path)

        return output

    @property
    def tdb_labels(
        self
    ) -> list[str]:

        '''
        Returns the list of labels from the topographic database index map.
        '''

        output = list(self.indexmap_tdb['label'])

        return output

    def is_valid_label_tdb(
        self,
        label: str
    ) -> bool:

        '''
        Returns whether the label exists in the topographic database index map.

        Parameters
        ----------
        label : str
            Name of the label.

        Returns
        -------
        bool
            True if the label exists, False otherwise.
        '''

        return label in self.tdb_labels

    def dem_download_by_labels(
        self,
        labels: list[str],
        folder_path: str,
        http_headers: typing.Optional[dict[str, str]] = None
    ) -> bool:

        '''
        Downloads the DEM raster files for the given labels.

        Parameters
        ----------
        labels : list of str
            List of label names from the DEM index map.

        folder_path : str
            Complete folder path to save the downloaded raster files.

        http_headers : dict, optional
            HTTP headers to be used for the web request. If not provided, the default headers
            :attr:`SuomiGeoData.core.Core.default_http_headers` will be used.

        Returns
        -------
        bool
            True if all the DEM raster files were successfully downloaded and
            exist at the specified folder path, False otherwise.
        '''

        # check whether the input labels exist
        for label in labels:
            if self.is_valid_label_dem(label):
                pass
            else:
                raise Exception(
                    f'The label "{label}" does not exist in the index map.'
                )

        # check the existence of the given folder path
        if os.path.isdir(folder_path):
            pass
        else:
            raise Exception(
                f'The folder path "{folder_path}" is not a valid directory.'
            )

        # web request headers
        if http_headers is None:
            headers = Core().default_http_headers
        else:
            headers = http_headers

        # download topographic database
        suffix_urls = self.indexmap_dem[self.indexmap_dem['label'].isin(labels)]['path']
        count = 1
        for label, url in zip(labels, suffix_urls):
            label_url = Core()._url_prefix_paituli_dem_tdb + url
            response = requests.get(
                url=label_url,
                headers=headers
            )
            label_file = os.path.join(
                folder_path, f'{label}.tif'
            )
            with open(label_file, 'wb') as label_raster:
                label_raster.write(response.content)
            print(
                f'Download of label {label} completed (count {count}/{len(labels)}).'
            )
            count = count + 1

        output = all(os.path.isfile(os.path.join(folder_path, f'{label}.tif')) for label in labels)

        return output

    def tdb_download_by_labels(
        self,
        labels: list[str],
        folder_path: str,
        http_headers: typing.Optional[dict[str, str]] = None
    ) -> bool:

        '''
        Downloads the topographic database folders of shapefiles for the given labels.

        Parameters
        ----------
        labels : list of str
            List of label names from the topographic database index map.

        folder_path : str
            Complete folder path to save the downloaded folder of shapefiles.

        http_headers : dict, optional
            HTTP headers to be used for the web request. If not provided, the default headers
            :attr:`SuomiGeoData.core.Core.default_http_headers` will be used.

        Returns
        -------
        bool
            True if all the topographic database folders were successfully downloaded and
            exist at the specified folder path, False otherwise.
        '''

        # check whether the input labels exist
        for label in labels:
            if self.is_valid_label_tdb(label):
                pass
            else:
                raise Exception(
                    f'The label "{label}" does not exist in the index map.'
                )

        # check the existence of the given folder path
        if os.path.isdir(folder_path):
            pass
        else:
            raise Exception(
                f'The folder path "{folder_path}" is not a valid directory.'
            )

        # web request headers
        if http_headers is None:
            headers = Core().default_http_headers
        else:
            headers = http_headers

        # download topographic database
        suffix_urls = self.indexmap_tdb[self.indexmap_tdb['label'].isin(labels)]['path']
        count = 1
        for label, url in zip(labels, suffix_urls):
            label_url = Core()._url_prefix_paituli_dem_tdb + url
            response = requests.get(
                url=label_url,
                headers=headers
            )
            label_data = io.BytesIO(response.content)
            with zipfile.ZipFile(label_data, 'r') as label_zip:
                label_zip.extractall(
                    os.path.join(folder_path, label)
                )
            print(
                f'Download of label {label} completed (count {count}/{len(labels)}).'
            )
            count = count + 1

        output = all(os.path.isdir(os.path.join(folder_path, label)) for label in labels)

        return output
