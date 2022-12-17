#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 22:03:56 2022

@author: wwelsh
"""

import requests
import re
import pandas as pd
import datetime
import time
import cloudscraper
import numpy as np



Trade_Matrix = pd.read_excel(r'/Users/wwelsh/Desktop/ARTG5330/Final Project/Overall Trade Summary.xlsx')


Full_Transaction_Data = pd.DataFrame()
Team_List = ['ATL', 'BOS', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET',
             'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL',
             'MIN', 'NJN', 'NOH', 'NYK', 'OKC', 'ORL', 'PHI', 'PHO',
             'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']

for Team in Team_List:
    Transaction_Data = Trade_Matrix[['Team_1',Team]]
    Transaction_Data.rename(columns = {Team:'Total Trades'}, inplace = True)
    Transaction_Data['Team_2'] = Team
    Full_Transaction_Data = Full_Transaction_Data.append(Transaction_Data)
    
Full_Transaction_Data.dropna(inplace = True)

Color_Key = pd.read_excel(r'/Users/wwelsh/Desktop/ARTG5330/Final Project/Team Color Key.xlsx')
Color_Key['org_x'] = -Color_Key['org_x']
Color_Key['org_y'] = -Color_Key['org_y']

Color_Key.loc[Color_Key['Team_1']=='HOU', 'org_y']  =  Color_Key['org_y']+2
Color_Key.loc[Color_Key['Team_1']=='SAS', 'org_x']  =  Color_Key['org_x']-2
Color_Key.loc[Color_Key['Team_1']=='LAC', 'org_x']  =  Color_Key['org_x']-2
Color_Key.loc[Color_Key['Team_1']=='LAL', 'org_x']  =  Color_Key['org_x']+2
Color_Key.loc[Color_Key['Team_1']=='LAL', 'org_y']  =  Color_Key['org_y']+2
Color_Key.loc[Color_Key['Team_1']=='CHA', 'org_x']  =  Color_Key['org_x']+1
Color_Key.loc[Color_Key['Team_1']=='CHA', 'org_y']  =  Color_Key['org_y']+1
Color_Key.loc[Color_Key['Team_1']=='SAC', 'org_y']  =  Color_Key['org_y']-2
Color_Key.loc[Color_Key['Team_1']=='MIL', 'org_y']  =  Color_Key['org_y']-2
Color_Key.loc[Color_Key['Team_1']=='DET', 'org_y']  =  Color_Key['org_y']-2
Color_Key.loc[Color_Key['Team_1']=='NJN', 'org_x']  =  Color_Key['org_x']+3
Color_Key.loc[Color_Key['Team_1']=='NJN', 'org_y']  =  Color_Key['org_y']+1.5
Color_Key.loc[Color_Key['Team_1']=='NYK', 'org_y']  =  Color_Key['org_y']-1
Color_Key.loc[Color_Key['Team_1']=='WAS', 'org_y']  =  Color_Key['org_y']+2.75
Color_Key.loc[Color_Key['Team_1']=='PHI', 'org_y']  =  Color_Key['org_y']+1
Color_Key.loc[Color_Key['Team_1']=='BOS', 'org_x']  =  Color_Key['org_x']+1
Color_Key.loc[Color_Key['Team_1']=='T0R', 'org_y']  =  Color_Key['org_y']-1
Color_Key.loc[Color_Key['Team_1']=='TOR', 'org_x']  =  Color_Key['org_x']+1.5
Color_Key.loc[Color_Key['Team_1']=='P0R', 'org_x']  =  Color_Key['org_x']+1
Color_Key.loc[Color_Key['Team_1']=='GSW', 'org_x']  =  Color_Key['org_x']+.5


Full_Transaction_Data = Full_Transaction_Data.merge(Color_Key, on = 'Team_1')


#Teams['org_x'] = np.random.randint(0,100, size=len(Teams))
#Teams['org_y'] = np.random.randint(0,100, size=len(Teams))

Teams2 = Color_Key[['Team_1','NBA_Team_Name','org_x','org_y']].rename(columns = {'Team_1':'Team_2','NBA_Team_Name':'NBA_Team_Name_2', 'org_x':'dest_x','org_y':'dest_y'})

#Full_Transaction_Data = Full_Transaction_Data.merge(Teams, on = 'Team_1')
Full_Transaction_Data = Full_Transaction_Data.merge(Teams2, on = 'Team_2')

Full_Transaction_Data.to_json('All_Transaction_Data.json', orient = 'records')

Team_Summaries = pd.pivot_table(Full_Transaction_Data, values = ['Total Trades'],
                                index = ['Team_1','NBA_Team_Name','org_x','org_y','Border_Color','Fill_Color'],
                                aggfunc = np.sum).reset_index()
Team_Summaries.to_json('Team_Summaries.json', orient = 'records')
