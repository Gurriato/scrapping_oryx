# -*- coding: utf-8 -*-
"""
Este script tiene como objetivo raspar información de dos artículos específicos
sobre equipos de origen ruso y ucraniano. La información se extrae, transforma
y almacena en DataFrames de pandas.

Created on Wed Aug 23 14:24:10 2023
@author: gblancom
"""

import pandas as pd
import gc
import tools
import json
import datetime as dt
import re
from ydata_profiling import ProfileReport
import matplotlib


import configparser

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

column_order = ['owner', 'origen', 'weapon', 'platform', 'total', 'number', 'Status', 'url']

# Russia scrap
urlRU = 'https://www.oryxspioenkop.com/2022/02/attack-on-europe-documenting-equipment.html'
scraped_object = tools.extract_lists_from_article(urlRU)
RU, total_RU = tools.trans_to_df(scraped_object)
RU['origen'] = RU['origen'].apply(tools.extr_country)
RU[['total', 'platform']] = RU['platform'].str.extract(r'(\d+)\s?([^:]+)', expand=True)
RU['owner'] = 'RU'
RU = RU[column_order]

# Ucrania scrap
urlUA = 'https://www.oryxspioenkop.com/2022/02/attack-on-europe-documenting-ukrainian.html'
scraped_object = tools.extract_lists_from_article(urlUA)
UA, total_UA = tools.trans_to_df(scraped_object)
UA['origen'] = UA['origen'].apply(tools.extr_country)
UA[['total', 'platform']] = UA['platform'].str.extract(r'(\d+)\s?([^:]+)', expand=True)
UA['owner'] = 'UA'
UA = UA[column_order]

# concat and final cleaning
to_file = pd.concat([RU, UA])
to_file = to_file.reset_index(drop=True)
to_file['url'] = to_file['url'].apply(tools.clean_url)

# Memory
scraped_object, UA, RU = None, None, None
gc.collect()


to_report = to_file.copy()
to_report['Status'] = to_report['Status'].astype(str)
to_report['origen'] = to_report['origen'].astype(str)
outcome = tools.insertar_en_bbdd(to_report, config['usuario'], config['pass'], config['host'], config['database'], 'bajas')
now = dt.datetime.now()
to_file.to_csv('./Data/scrap_raw_' + str(now.date()) + '.csv')

# Transforming Totals
regex = r"^(.+?)\s*\((\d+), of which( destroyed: (\d+))?(, damaged: (\d+))?(, abandoned: (\d+))?(, captured: (\d+))?\)$"
total_RU = pd.Series(total_RU)
total_RU = total_RU.str.extract(regex)
total_RU.columns = ['Type', 'Total', 'd1', 'Destroyed', 'd2', 'Damaged', 'd3', 'Abandoned', 'd4', 'Captured']
total_RU.drop(['d1', 'd2', 'd3', 'd4'], axis=1, inplace=True)
total_RU = total_RU[1:]
total_RU.fillna(0, inplace=True)
total_RU[['Total', 'Destroyed', 'Damaged', 'Abandoned', 'Captured']] = total_RU[['Total', 'Destroyed', 'Damaged', 'Abandoned', 'Captured']].astype(int)
outcome = tools.insertar_en_bbdd(total_RU, config['usuario'], config['pass'], config['host'], config['database'], 'totals_RU')
total_RU.to_csv('./Data/scrap_Total_RU' + str(now.date()) + '.csv')

total_UA = pd.Series(total_UA)
total_UA = total_UA.str.extract(regex)
total_UA.columns = ['Type', 'Total', 'd1', 'Destroyed', 'd2', 'Damaged', 'd3', 'Abandoned', 'd4', 'Captured']
total_UA.drop(['d1', 'd2', 'd3', 'd4'], axis=1, inplace=True)
total_UA = total_UA[1:]
total_UA.fillna(0, inplace=True)
total_UA[['Total', 'Destroyed', 'Damaged', 'Abandoned', 'Captured']] = total_UA[['Total', 'Destroyed', 'Damaged', 'Abandoned', 'Captured']].astype(int)
outcome = tools.insertar_en_bbdd(total_UA, config['usuario'], config['pass'], config['host'], config['database'], 'totals_UA')
total_UA.to_csv('./Data/scrap_Total_UA_' + str(now.date()) + '.csv')

#from ydata_profiling import ProfileReport
#report = pd.read_csv(r'C:\Users\gblancom\PycharmProjects\pythonProject\scrap_raw.csv')
#profile = ProfileReport(report, title="Informe de perfil de pandas")
#profile.to_file(r'C:\Users\gblancom\PycharmProjects\pythonProject\informe.html')

