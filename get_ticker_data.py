# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 13:20:27 2020

@author: JOAO VICTOR
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import pandas as pd
import pyfolio as pf
import yfinance as yf
import pandas_datareader.data as web
import warnings



scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name(r'C:\Users\JOAO VICTOR\Desktop\quant-trade\token.json', scope)
client = gspread.authorize(creds)

sheet = client.open('Quant').sheet1

ticker2016 = ['TIET11','BTOW3','BBAS3', 'BBDC3', 'BRKM3', 'BRFS3', 'CCRO3', 'CMIG3',
          'CESP3', 'CIEL3', 'CPLE3', 'CPFE3', 'DTEX3', 'ECOR3', 'ENBR3', 'ELET3',
          'EMBR3', 'EVEN3', 'SUZB3', 'FLRY3', 'ITSA4', 'ITUB3', 'KLBN11',
          'LAME4', 'LIGT3', 'OIBR4', 'LREN3', 'SANB11', 'SULA11', 'VIVT4',
          'TIMP3', 'EGIE3', 'WEGE3' ]

def get_ticker_df(lista_ticker):

    dic_price = {}

    def get_ticker_prices(ticker, price = True):

        sheet.update_cell(1, 2, '{}'.format(ticker))
        time.sleep(5)
        price_close = sheet.col_values(5)[2:]
        date_close = sheet.col_values(4)[2:]
        if price == True:
            return price_close
        else:
            return date_close
    maxdate = [0]
    for i in lista_ticker:

        prices = get_ticker_prices(i)
        dic_price['{}'.format(i)] = prices

        date = get_ticker_prices(i, price=False)

        if len(date) > len(maxdate):
            maxdate = date

    df = pd.DataFrame.from_dict(dic_price, orient = 'index')
    df = df.transpose().astype(float)
    df.index = maxdate
    return df



#Cálculo de retorno por uma ação
'''dados_google = get_ticker_df(ticker2016)


retorno = dados_google.pct_change()

retorno_acumulado = (1 + retorno).cumprod()
retorno_acumulado.iloc[0] = 1

carteira = 10000*retorno_acumulado
carteira['saldo'] = carteira.sum(axis=1)
carteira['retorno'] = carteira['saldo'].pct_change()
retorno_port = pd.Series(carteira['retorno'])


ibov = ['IBOV']
dados_ibov = get_ticker_df(ibov)

bench = dados_ibov.pct_change()

bench_acumulado = (1+bench).cumprod()
bench_acumulado.iloc[0] = 1

carteira_ibov = 10000*bench_acumulado
carteira_ibov['retorno'] = carteira_ibov.pct_change()


pf.create_full_tear_sheet(retorno_port, benchmark_rets=carteira_ibov['retorno'])
'''



