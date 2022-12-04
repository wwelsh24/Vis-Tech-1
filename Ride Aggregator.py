#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 03:05:43 2022

@author: wwelsh
"""

import numpy as np
import time
from datetime import datetime
import geopandas as gpd
import pandas as pd
from shapely import wkt

October_Trip_Data = pd.read_excel(r"/Users/wwelsh/Desktop/ARTG5330/Project 2/Trip Data/202210-bluebikes-tripdata.xlsx")
Location_Station_Key = pd.read_excel(r'/Users/wwelsh/Desktop/ARTG5330/Project 2/Location_Station_Key.xlsx')
Week_Day_Key = pd.read_excel(r'/Users/wwelsh/Desktop/ARTG5330/Project 2/Week_Day_Key.xlsx')

Trip_Data_With_Location = October_Trip_Data.merge(Location_Station_Key, how = 'left', left_on = 'start station name',
                                                  right_on = 'Name')
Trip_Data_With_Location.rename(columns = {'Location':'Origin'}, inplace = True)

Trip_Data_With_Location = Trip_Data_With_Location.merge(Location_Station_Key, how = 'left', left_on = 'end station name',
                                                  right_on = 'Name')
Trip_Data_With_Location.rename(columns = {'Location':'Destination'}, inplace = True)

Trip_Data_With_Location['Start Date'] = Trip_Data_With_Location['starttime'].dt.date.astype(str)
Trip_Data_With_Location['Week Day Number'] = Trip_Data_With_Location['starttime'].dt.dayofweek

Trip_Data_With_Location = Trip_Data_With_Location.merge(Week_Day_Key, how = 'inner')

Trip_Data_With_Location['Start Date'] = Trip_Data_With_Location['Start Date']+ ' '+ Trip_Data_With_Location['Week Day']

Trip_Data_With_Location['Hour'] = Trip_Data_With_Location['starttime'].dt.hour
Trip_Data_With_Location['Rides'] = 1

Daily_Trip_Summaries = pd.pivot_table(Trip_Data_With_Location, values=['Rides'],
                                      index=['Start Date','Origin','Destination'],
                                      aggfunc=np.sum).reset_index()

Daily_Trip_Summaries.to_json('October Daily Rides.json', orient = 'records')

Hourly_Trip_Summaries = pd.pivot_table(Trip_Data_With_Location, values=['Rides'],
                                      index=['Hour','Origin','Destination'],
                                      aggfunc=np.sum).reset_index()

Hourly_Trip_Summaries.to_json('October Hourly Rides.json', orient = 'records')

Daily_Hourly_Trip_Summaries = pd.pivot_table(Trip_Data_With_Location, values=['Rides'],
                                      index=['Start Date','Hour','Origin','Destination'],
                                      aggfunc=np.sum).reset_index()

Daily_Hourly_Trip_Summaries.to_json('October Daily-Hourly Rides.json', orient = 'records')

Test_Data = Trip_Data_With_Location.head(10)