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
import numpy as np

ticker2016 = ['TIET11.SA','BTOW3.SA','BBAS3.SA']
dados_yahoo = web.get_data_yahoo(ticker2016, start='2016-01-01', end='2017-01-01')['Adj Close']


ibov2016 = ['^BVSP']
dados_ibov = web.get_data_yahoo(ibov2016, start='2016-01-01', end='2017-01-01')['Adj Close']

lista = [1.0, 0.0, 0.00]

def backtest(df_ticker, df_ibov, lista_pct):

    lista_pct = np.array(lista_pct).reshape(1, 3)

    retorno = df_ticker.pct_change()
    retorno_acumulado = (1 + retorno).cumprod()
    retorno_acumulado.iloc[0] = 1

    carteira = retorno_acumulado.multiply(lista, axis = 1)
    carteira['saldo'] = carteira.sum(axis=1)
    carteira['retorno'] = carteira['saldo'].pct_change()

    retorno_ibov = df_ibov.pct_change()
    retorno_acumulado_ibov = (1 + retorno_ibov).cumprod()
    retorno_acumulado_ibov.iloc[0] = 1

    carteira_ibov = retorno_acumulado_ibov

    carteira_ibov['saldo'] = carteira_ibov.sum(axis=1)
    carteira_ibov['retorno'] = carteira_ibov['saldo'].pct_change()

    return pf.create_full_tear_sheet(carteira['retorno'], benchmark_rets=carteira_ibov['retorno'])

backtest(dados_yahoo, dados_ibov, lista)