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

def maskCloudAndShadowsSR(image):
  cloudProb = image.select('MSK_CLDPRB')
  cloud = cloudProb.lt(10)
  scl = image.select('SCL')
  shadow = scl.eq(3) # 3 = cloud shadow
  cirrus = scl.eq(10) # 10 = cirrus
  mask = cloud.And(cirrus.neq(1)).And(shadow.neq(1))
  return image.updateMask(mask)

s2_data = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')\
         .filterBounds(roi)\
         .filterDate(startDate, endDate)\
         .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10))\
         .map(maskCloudAndShadowsSR)\
         .median().clip(roi)

ndvi = s2_data.select('NDVI')

geemap.ee_export_image_to_drive(
    image= ndvi,
    description='S2_ndvi_bands',
    folder= 'S2_Data_Folder',
    region=roi,
    scale=10,
    crs='EPSG:4326',
    maxPixels=1e13,
    fileFormat='GeoTIFF',
)