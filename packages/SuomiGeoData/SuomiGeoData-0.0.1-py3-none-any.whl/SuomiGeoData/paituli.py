import os
import geopandas
import typing
from .core import Core


class Paituli:

    '''
    Executes downloading and extracting data from Paituli (https://paituli.csc.fi/download.html).

    Attributes:
    -----------
    index_td : GeoDataFrame
        A GeoDataFrame containing the topographical database index map.
    '''

    def __init__(
        self
    ) -> None:

        '''
        Initializes the class by loading the topographical index map.
        '''

        self.indexmap_tdb = geopandas.read_file(
            os.path.join(
                os.path.dirname(__file__), 'data', 'nls_td_index.shp'
            )
        )

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
