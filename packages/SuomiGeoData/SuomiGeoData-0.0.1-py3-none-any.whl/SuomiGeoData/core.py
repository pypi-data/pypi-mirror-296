import pyogrio


class Core:

    '''
    Core functionality of :mod:`SuomiGeoData` module.
    '''

    def is_valid_write_shape_driver(
        self,
        file_path: str
    ) -> bool:

        '''
        Returns whether the given file path is valid to write a GeoDataFrame.

        Parameters
        ----------
        file_path : str
            File path to save the GeoDataFrame.

        Returns
        -------
        bool
            True if the file path is valid, False otherwise.
        '''

        try:
            pyogrio.detect_write_driver(file_path)
            output = True
        except Exception:
            output = False

        return output
