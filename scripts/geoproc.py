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

##
# Note:  Update: On 6th April 2016
#
#  GDALTransform is for coordinate transformation.
#
#    Xgeo = GT(0) + Xpixel*GT(1) + Yline*GT(2)
#    Ygeo = GT(3) + Xpixel*GT(4) + Yline*GT(5)
#
# Pixel and line are found with inverse transform. So with already known Xgeo,
# need to find pixel = (Xgeo - gt[0])/gt[1], width is the amount of coordinates that
# covers the pixel.
# Run gdalinfo on geoTIFF :
#   Origin = (-180.004166669999989,90.004166670000004)
#   Pixel Size = (0.083333333333000,-0.083333333333000)
#
# Upper left point is at lon= -180, and lat=90, each pixel is 0.0833 in lat and long.
# Four pixels to the right would be lon = -180 + 4 * 0.0833
#
##
