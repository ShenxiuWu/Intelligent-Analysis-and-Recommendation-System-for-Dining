#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import folium
import pandas as pd 
import geopandas as gpd
from folium.plugins import HeatMap

for_map = pd.read_csv('./rest_business.csv')
congr_districts = gpd.read_file('zip://'+'./cb_2016_us_cd115_20m.zip')

# Set datum and projection info for census.gov 2015 Tiger data
congr_districts.crs = {'datum': 'NAD83', 'ellps': 'GRS80', 'proj':'longlat', 'no_defs':True}

# Filter out all but the district of interest
district23 = congr_districts[ congr_districts.GEOID == '3201' ]  # 36 = NY, 23 = District
distric_map = folium.Map(location=[36, -115], zoom_start=7, tiles='cartodbpositron' )
# convert it to the projection of our folium openstreetmap
district23 = district23.to_crs({'init':'epsg:3857'}) 
max_amount = float(for_map['stars'].max())

hmap = folium.Map(location=[36.15, -115.15], zoom_start=10 )
i = 0
los = []
while i<5682:
    zipped = zip(for_map.latitude.values, for_map.longitude.values, for_map.stars.values)
    los.append(list(tuple(zipped)[i]))
    i=i+1
HeatMap(los, 
        min_opacity=0.0001,
        max_val=5.0,
        radius=18, blur=42, 
        max_zoom=1, 
        #gradient={.6: 'blue', .8: 'lime', .95: 'red'}
        ).add_to(hmap)
hmap.save("heatmap.html")
hmap
