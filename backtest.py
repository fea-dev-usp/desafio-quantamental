# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 19:06:41 2020

@author: JOAO VICTOR
"""
import yfinance as yf
import pandas_datareader.data as web
import pandas as pd
import pyfolio as pf
import warnings

ticker2016 = ['TIET11.SA','BTOW3.SA','BBAS3.SA', 'BBDC3.SA', 'BRKM3.SA', 'BRFS3.SA', 'CCRO3.SA', 'CMIG3.SA',
          'CESP3.SA', 'CIEL3.SA', 'CPLE3.SA', 'CPFE3.SA', 'DTEX3.SA', 'ECOR3.SA', 'ENBR3.SA', 'ELET3.SA',
          'EMBR3.SA', 'EVEN3.SA', 'SUZB3.SA', 'FLRY3.SA', 'ITSA4.SA', 'ITUB3.SA', 'KLBN11.SA',
          'LAME4.SA', 'LIGT3.SA', 'OIBR4.SA', 'LREN3.SA', 'SANB11.SA', 'SULA11.SA', 'VIVT4.SA',
          'TIMP3.SA', 'EGIE3.SA', 'WEGE3.SA', 'SUZB3']
dados_yahoo = web.get_data_yahoo(ticker2016, start='2016-01-01', end='2017-01-01')['Adj Close']

def backtest(df_ticker, df_ibov, lista_pct):
    retorno = df_ticker
    retorno_acumulado = (1 + retorno).cumprod()
    retorno_acumulado.iloc[0] = 1

    carteira = 10000*lista_pct*retorno_acumulado

    carteira['saldo'] = carteira.sum(axis=1)
    carteira['retorno'] = carteira['saldo'].pct_change()

    retorno_ibov = df_ibov
    retorno_acumulado_ibov = (1 + retorno_ibov).cumprod()
    retorno_acumulado_ibov.iloc[0] = 1

    carteira_ibov = 10000*retorno_acumulado_ibov

    carteira_ibov['saldo'] = carteira_ibov.sum(axis=1)
    carteira_ibov['retorno'] = carteira_ibov['saldo'].pct_change()

    return pf.create_full_tear_sheet(carteira['retorno'], benchmark_rets=carteira_ibov['retorno'])