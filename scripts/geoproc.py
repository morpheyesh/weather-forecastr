import os, sys, time, gdal
from gdalconst import *


def elevation_data(coRd):

  #provide with coordinates
  lat = float(coRd[0])
  lon = float(coRd[1])

  gdal.AllRegister()

  # open the image
  ds = gdal.Open('elev.tif', GA_ReadOnly)

  if ds is None:
    print 'Could not open image'
    sys.exit(1)

  #getting the image details
  rows = ds.RasterYSize
  cols = ds.RasterXSize
  bands = ds.RasterCount


  ##Getting the georefinformation - Use affine transformation matrix  - pixel coords to world coords
  tr0 = ds.GetGeoTransform()
  xOrigin = tr0[0]
  yOrigin = tr0[3]
  pixelWidth = tr0[1]
  pixelHeight = tr0[5]
  ##Convert to raster points
  pixel = int((lat - xOrigin) / pixelWidth)
  line = int((lon - yOrigin) / pixelHeight)
  #pixel and line
  b = ds.GetRasterBand(1)

  dat = b.ReadAsArray(3341, 1244, 1, 1)
  return dat ##this is wrong, this is giving me zero everytime? am i making a fundamental mistake? revisit!
