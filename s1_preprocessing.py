import ee
import geemap

ee.Authenticate()
ee.Initialize(project='ee-prasad007nr')

roi =  ee.Geometry.Polygon(
        [[[77.73737417379047, 13.339028922046372],
          [77.73737417379047, 13.212721128596087],
          [77.86921011129047, 13.212721128596087],
          [77.86921011129047, 13.339028922046372]]])

startDate = '2025-01-01'
endDate = '2025-01-31'

s1_data = ee.ImageCollection('COPERNICUS/S1_GRD')\
              .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV')) \
              .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH')) \
              .filter(ee.Filter.eq('instrumentMode', 'IW')) \
              .filterBounds(roi)\
              .filterDate(startDate, endDate)\
              .median().clip(roi)\
              .select(['VV','VH'])

guassian_filter = ee.Kernel.gaussian(radius = 50, sigma = 1, units = 'meters', normalize = True)

filtered = s1_data.convolve(guassian_filter)

vv_data = filtered.select('VV')
vh_data = filtered.select('VH')

vh_int = vh_data.multiply(100).int()
glcm_texture = vh_int.glcmTexture(**{'size': 3})
texture_bands = glcm_texture.select(['VH_savg', 'VH_var', 'VH_asm', 'VH_contrast', 'VH_diss', 'VH_ent', 'VH_corr'])

vv_int = vv_data.multiply(100).int()
glcm_texture = vv_int.glcmTexture(**{'size': 3})
texture_bands = glcm_texture.select(['VV_savg', 'VV_var', 'VV_asm', 'VV_contrast', 'VV_diss', 'VV_ent', 'VV_corr'])

geemap.ee_export_image_to_drive(
    image= texture_bands,
    description='S1_texture_bands',
    folder= 'S1_Data_Folder',
    region=roi,
    scale=10,
    crs='EPSG:4326',
    maxPixels=1e13,
    fileFormat='GeoTIFF',
)