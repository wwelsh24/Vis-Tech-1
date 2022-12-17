#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 19:44:22 2022

@author: wwelsh
"""

import requests
import re
import pandas as pd
import datetime
import time
import cloudscraper

scraper = cloudscraper.create_scraper(delay=10)  # returns a CloudScraper instance
# Or: scraper = cloudscraper.CloudScraper()  # CloudScraper inherits from requests.Session
url = "https://www.basketball-reference.com/friv/trades.fcgi?f1="+'ATL'+"&f2="+'BOS'
print(scraper.get(url).text)

Season_Key = pd.read_excel('/Users/wwelsh/Desktop/ARTG5330/Final Project/Season Key.xlsx')
Season_Key['Join Key'] = 1

Full_Transaction_Data = pd.DataFrame()
Team_List = ['ATL', 'BOS', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET',
             'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL',
             'MIN', 'NJN', 'NOH', 'NYK', 'OKC', 'ORL', 'PHI', 'PHO',
             'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']


for T1 in Team_List[0:5]:
    print(T1+' Start Time: ',datetime.datetime.now())
    for T2 in Team_List[0:5]:
        time.sleep(10)
        if T1 == T2:
            continue
        else:
            url = "https://www.basketball-reference.com/friv/trades.fcgi?f1="+T1+"&f2="+T2
            r = requests.get(url)
            print(url)
            print(len(r.text))
            
            Trades = re.findall('(?<=<p class="transaction ">)(.*)(?=</p>)',r.text)
            New_HTML = ['<p class = "BBRef_Info">' + tr for tr in Trades]
            New_HTML = [tr+'</p>' for tr in New_HTML]
            
            Team1 = [T1]*len(Trades)
            Team2 = [T2]*len(Trades)
            
            Dates = re.findall('(?<=<strong>)[A-Za-z]{3,} [0-9]{1,2}, [0-9]{4}(?=</strong>)', r.text)
            
            Transaction_Data = pd.DataFrame(list(zip(Team1, Team2, Dates, New_HTML)), columns =['Team_1', 'Team_2','Transaction Date', 'BBR_HTML'])
            
            Transaction_Data['Transaction Date'] = pd.to_datetime(Transaction_Data['Transaction Date'],infer_datetime_format=True)
            Transaction_Data['Join Key'] = 1
            
            Transaction_Data = Transaction_Data.merge(Season_Key, on = 'Join Key')
            Transaction_Data = Transaction_Data.loc[(Transaction_Data['Transaction Date']>=Transaction_Data['Start Date'])&
                                                    (Transaction_Data['Transaction Date']<=Transaction_Data['End Date'])]
            Transaction_Data = Transaction_Data[['Team_1','Team_2','Season','Transaction Date','BBR_HTML']]
            Full_Transaction_Data = Full_Transaction_Data.append(Transaction_Data)






#<strong>August 7, 2018</strong>
#Trades = re.findall('<p class="transaction ">^(.*?)</p>',r.text)