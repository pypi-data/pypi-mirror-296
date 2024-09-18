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

    @property
    def _url_prefix_paituli_dem_tdb(
        self,
    ) -> str:

        '''
        Returns the prefix url for downloading files
        based on DEM and topographic database labels.
        '''

        output = 'https://www.nic.funet.fi/index/geodata/'

        return output

    @property
    def default_http_headers(
        self,
    ) -> dict[str, str]:

        '''
        Returns the default http headers to be used for the web requests.
        '''

        output = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
            'Host': 'www.nic.funet.fi',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Connection': 'keep-alive'
        }

        return output
