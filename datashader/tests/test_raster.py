from os import path

import pytest
import datashader as ds
import rasterio as rio

from pytest import set_trace

BASE_PATH = path.split(__file__)[0]
DATA_PATH = path.abspath(path.join(BASE_PATH, 'data'))
TEST_RASTER_PATH = path.join(DATA_PATH, 'world.rgb.tif')

with rio.open(TEST_RASTER_PATH) as src:
    x_range = (src.bounds.left, src.bounds.right)
    y_range = (src.bounds.bottom, src.bounds.top)
    cvs = ds.Canvas(plot_width=2,
                    plot_height=2,
                    x_range=x_range,
                    y_range=y_range)

def test_raster_aggregate_default():
    with rio.open(TEST_RASTER_PATH) as src:
        agg = cvs.raster(src)
        assert agg is not None

def test_raster_aggregate_nearest():
    with rio.open(TEST_RASTER_PATH) as src:
        agg = cvs.raster(src, resample_method='nearest')
        assert agg is not None

def test_raster_aggregate_with_overviews():
    with rio.open(TEST_RASTER_PATH) as src:
        agg = cvs.raster(src, use_overviews=True)
        assert agg is not None

def test_raster_aggregate_without_overviews():
    with rio.open(TEST_RASTER_PATH) as src:
        agg = cvs.raster(src, use_overviews=False)
        assert agg is not None

def test_raster_set_missing():
    with rio.open(TEST_RASTER_PATH) as src:
        agg = cvs.raster(src, missing=-100)
        assert agg is not None

def test_out_of_bounds_return_correct_size():
    with rio.open(TEST_RASTER_PATH) as src:
        cvs = ds.Canvas(plot_width=2,
                        plot_height=2,
                        x_range=[1e10, 1e20],
                        y_range=[1e10, 1e20])
        agg = cvs.raster(src, missing=-100)
        assert agg.shape == (2,2)
        assert agg is not None

def test_partial_extent_returns_correct_size():
    with rio.open(TEST_RASTER_PATH) as src:
        half_width = (src.bounds.right - src.bounds.left) / 2
        half_height = (src.bounds.top - src.bounds.bottom) / 2
        cvs = ds.Canvas(plot_width=512,
                        plot_height=256,
                        x_range=[src.bounds.left-half_width, src.bounds.left+half_width],
                        y_range=[src.bounds.bottom-half_height, src.bounds.bottom+half_height])
        agg = cvs.raster(src, missing=-100)
        assert agg.shape == (256, 512)
        assert agg is not None


