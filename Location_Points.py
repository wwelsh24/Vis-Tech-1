#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 22:06:07 2022

@author: wwelsh
"""

import numpy as np
import time
from datetime import datetime
import geopandas as gpd
import pandas as pd
from shapely import wkt

Neighborhood_Key = pd.read_excel(r"/Users/wwelsh/Desktop/ARTG5330/Project 2/Relevant_Locations_2.xlsx", sheet_name = 'Neighborhoods')
Location_Key = pd.read_excel(r"/Users/wwelsh/Desktop/ARTG5330/Project 2/Relevant_Locations_2.xlsx", sheet_name = 'Locations')
#https://stackoverflow.com/questions/68207623/extract-coordinates-of-the-center-of-polygons-in-a-geojson-file-in-python
Towns = gpd.read_file("https://raw.githubusercontent.com/NewtonMAGIS/GISData/master/Massachusetts%20Town%20Boundaries/MassTowns.geojson")

#https://gis.stackexchange.com/questions/404299/how-to-convert-string-type-to-shapely-object
Stations = pd.read_csv('https://s3.amazonaws.com/hubway-data/current_bluebikes_stations.csv',header=1)

Stations_gdf = gpd.GeoDataFrame(Stations, geometry=gpd.points_from_xy(Stations.Longitude, Stations.Latitude), crs='epsg:4326')

Towns.head(2)

Towns["lon"] = Towns["geometry"].centroid.x
Towns["lat"] = Towns["geometry"].centroid.y
Towns['Area'] = Towns.area
Towns['Location'] = Towns.TOWN.str.title()
Towns = Towns.loc[Towns['Location']!='Boston']


Neighborhoods = gpd.read_file("https://bostonopendata-boston.opendata.arcgis.com/datasets/boston::boston-neighborhoods.geojson?outSR=%7B%22latestWkid%22%3A2249%2C%22wkid%22%3A102686%7D")
Neighborhoods["lon"] = Neighborhoods["geometry"].centroid.x
Neighborhoods["lat"] = Neighborhoods["geometry"].centroid.y
Test_Neighborhoods = Neighborhoods.head(2)
Neighborhoods = Neighborhoods.merge(Neighborhood_Key, how = 'inner')

Relevant_Locations = Towns[['Location','lon','lat', 'geometry']].append(Neighborhoods[['Location','lon','lat','geometry']])
Relevant_Locations = Relevant_Locations.merge(Location_Key, how = 'inner')


Location_Merge = Stations_gdf.sjoin(Relevant_Locations, how="inner", predicate='intersects')


Location_Station_Key = Location_Merge[['Name','Location']]
Location_Station_Key.to_excel('Location_Station_Key.xlsx', index = False)


Location_Coordinates = pd.pivot_table(Location_Merge, values=['Longitude','Latitude'], index=['Location'],
 aggfunc=np.mean).reset_index()

Salem_DF = Location_Coordinates.loc[Location_Coordinates['Location']=='Salem']
Salem_DF['X'] = 865
Salem_DF['Y'] = 25
Location_Coordinates = Location_Coordinates.loc[Location_Coordinates['Location']!='Salem']
Location_Coordinates['X'] = (Location_Coordinates['Longitude']-Location_Coordinates['Longitude'].min())/(Location_Coordinates['Longitude'].max()-Location_Coordinates['Longitude'].min())*850+25
Location_Coordinates['Y'] = 675-(Location_Coordinates['Latitude']-Location_Coordinates['Latitude'].min())/(Location_Coordinates['Latitude'].max()-Location_Coordinates['Latitude'].min())*650

#Manual Adjustments for visual clarity
Location_Coordinates.loc[Location_Coordinates['Location']!='Newton', 'X'] = Location_Coordinates['X']-40
Location_Coordinates.loc[Location_Coordinates['Location']=='Newton', 'X'] = Location_Coordinates['X']+10
Location_Coordinates.loc[Location_Coordinates['Location']=='Roxbury', 'Y'] = Location_Coordinates['Y']+15
Location_Coordinates.loc[Location_Coordinates['Location']=='Brookline', 'Y'] = Location_Coordinates['Y']+40
Location_Coordinates.loc[Location_Coordinates['Location']=='Brookline', 'X'] = Location_Coordinates['X']-40
Location_Coordinates.loc[Location_Coordinates['Location']=='Cambridge','Y'] = Location_Coordinates['Y']-40
Location_Coordinates.loc[Location_Coordinates['Location']=='Cambridge', 'X'] = Location_Coordinates['X']-80
Location_Coordinates.loc[Location_Coordinates['Location']=='Allston/Brighton', 'X'] = Location_Coordinates['X']-80
Location_Coordinates.loc[Location_Coordinates['Location']=='South Boston/Seaport','Y'] = Location_Coordinates['Y']+100
Location_Coordinates.loc[Location_Coordinates['Location']=='Downtown Area','X'] = Location_Coordinates['X']+40
Location_Coordinates.loc[Location_Coordinates['Location']=='Longwood/Fenway','Y'] = Location_Coordinates['Y']+15
Location_Coordinates.loc[Location_Coordinates['Location']=='Hyde Park','Y'] = Location_Coordinates['Y']-20

Location_Coordinates = Location_Coordinates.append(Salem_DF)
Location_Coordinates.to_json('Location_Coordinate_Key_4.json', orient = 'records')

Color_Key = pd.read_excel(r'Location_Color_Key.xlsx')
Color_Key.to_json('Location Color Key.json', orient = 'records')

