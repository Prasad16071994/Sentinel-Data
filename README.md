# Sentinel-1 and Sentinel-2 Processing Pipeline

## Overview
This project implements a preprocessing pipeline for:

- Sentinel-1 GRD (SAR) data
- Sentinel-2 Surface Reflectance data

Processing is performed using Google Earth Engine (GEE) and exported as GeoTIFF.

## Sentinel-1 Processing
- Filter by ROI and date
- Gaussian smoothing
- GLCM texture extraction (size = 3)
- Export texture bands

## Sentinel-2 Processing
- Cloud and shadow masking using SCL and cloud probability
- Median composite
- NDVI extraction
- Export as GeoTIFF

## How to Run

1. Install dependencies:
   pip install -r requirements.txt

2. Authenticate Earth Engine:
   earthengine authenticate

3. Run:
   python src/s1_data_downloading__&_processing.py
   python src/s2_data_downloading__&_processing.py