# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 13:20:27 2020

@author: JOAO VICTOR
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name('token.json', scope)
client = gspread.authorize(creds)

sheet = client.open('Quant').sheet1

data = sheet.get_all_records()

value_NA = sheet.row_values(1)

z = 0
x = 2

ticker2016 = ['TIET11','BTOW3','BBAS3', 'BBDC3', 'BRKM3', 'BRFS3', 'CCRO3', 'CMIG3',
          'CESP3', 'CIEL3', 'CPLE3', 'CPFE3', 'DTEX3', 'ECOR3', 'ENBR3', 'ELET3',
          'EMBR3', 'EVEN3', 'SUZB3', 'FLRY3', 'ITSA4', 'ITUB3', 'KLBN11',
          'LAME4', 'LIGT3', 'OIBR4', 'LREN3', 'SANB11', 'SULA11', 'VIVT4',
          'TIMP3', 'EGIE3', 'WEGE3' ]

df = pd.DataFrame()


for i in sheet.row_values(1):

    if i in ticker2016:

        df['Ação {}'.format(x)] = sheet.col_values(x)

    x += 1

