from typing import Optional

import os

import rasterio

from shapely.geometry import box

from .common import is_tiff
from geometry.change_crs import change_box_crs

from exceptions.type_checker import type_checker
from gis_typing.gis_types import CRS_TYPE

@type_checker
def get_transform(tiff_file: str):
    """
    Returns the affine transformer of a tiff file
    
    Parameters:
        tiff_file: (Relative) Path to the tiff file to read
    """
    if not is_tiff(tiff_file):
        raise Exception(f"{tiff_file} Is Not A Tiff File")

    if not os.path.isfile(tiff_file):
        raise Exception(f"Raster [{tiff_file}] Doesn't Exist")
    
    with rasterio.open(tiff_file) as src:
        transform = src.transform

    return transform

@type_checker
def get_crs(tiff_file: str):
    """
    Returns the affine crs of a tiff file
    
    Parameters:
        tiff_file: (Relative) Path to the tiff file to read
    """
    if not is_tiff(tiff_file):
        raise Exception(f"{tiff_file} Is Not A Tiff File")

    if not os.path.isfile(tiff_file):
        raise Exception(f"Raster [{tiff_file}] Doesn't Exist")
    
    with rasterio.open(tiff_file) as src:
        crs = src.crs

    return crs

@type_checker
def get_extent(tiff_file: str,
               crs: Optional[CRS_TYPE] = None):
    """
    Returns a shapely Polygon representing the extent of a given TIFF file.
    
    Parameters:
        tiff_file: (Relative) Path to the tiff file to read
        crs: crs in which to get the extent from. If None, the crs
            of the raster will be used.
    """
    if not is_tiff(tiff_file):
        raise Exception(f"{tiff_file} Is Not A Tiff File")

    if not os.path.isfile(tiff_file):
        raise Exception(f"Raster [{tiff_file}] Doesn't Exist")
    
    with rasterio.open(tiff_file) as src:
        tiff_crs = src.crs
        bbox = src.bounds
    
    if crs is not None:
        bbox = change_box_crs(bbox, tiff_crs, crs)

    return box(*bbox)