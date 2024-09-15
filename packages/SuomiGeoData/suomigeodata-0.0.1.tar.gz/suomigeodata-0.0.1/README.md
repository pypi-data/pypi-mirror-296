# SuomiGeoData

## What is SuomiGeoData?
SuomiGeoData is a Python package designed to simplify the process of downloading and extracting geospatial data from Suomi, that is Finland. The features of the package include:

- **[Paituli](https://paituli.csc.fi/download.html)** 
  - Accessing the topographic database index map.


## Easy Installation

To install, use pip:

```bash
pip install SuomiGeoData
```

## Quickstart
A brief example of how to start:

```python
>>> import SuomiGeoData
>>> paituli = SuomiGeoData.Paituli()

# get the topographic database index map
>>> im_tb = paituli.indexmap_tdb
>>> im_tb.shape
(3132, 3)
```

## Documentation


## Toolkit

