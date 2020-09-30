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
import datetime
from base_de_dados.importa_base import importa_base

def backtest(df_ticker, df_ibov, lista_pct):

    lista_pct = np.array(lista_pct).reshape(1, len(lista_pct))

    retorno = df_ticker.pct_change()
    retorno_acumulado = (1 + retorno).cumprod()
    retorno_acumulado.iloc[0] = 1

    carteira = retorno_acumulado.multiply(lista_pct, axis=1)
    carteira['saldo'] = carteira.sum(axis=1)
    carteira['retorno'] = carteira['saldo'].pct_change()

    retorno_ibov = df_ibov.pct_change()
    retorno_acumulado_ibov = (1 + retorno_ibov).cumprod()
    retorno_acumulado_ibov.iloc[0] = 1

    carteira_ibov = retorno_acumulado_ibov

    carteira_ibov['saldo'] = carteira_ibov.sum(axis=1)
    carteira_ibov['retorno'] = carteira_ibov['saldo'].pct_change()

    return carteira, carteira_ibov
    # return pf.create_full_tear_sheet(carteira['retorno'], benchmark_rets=carteira_ibov['retorno'])

if __name__ == '__main__':
    # ticker2016 = ['TIET11.SA','BTOW3.SA','BBAS3.SA']
    # ticker2016 = ['ABEV3.SA', 'B3SA3.SA']
    # dados_yahoo = web.get_data_yahoo(ticker2016, start='2016-01-01', end='2017-01-01')['Adj Close']
    #
    # ibov2016 = ['^BVSP']
    # dados_ibov = web.get_data_yahoo(ibov2016, start='2016-01-01', end='2017-01-01')['Adj Close']
    #
    # lista = [0.5, 0.5]

    # backtest(dados_yahoo, dados_ibov, lista)

    # TICKERS
    shares_tickers = ['ABEV3', 'AZUL4', 'B3SA3']
    index_tickers = ['IBOV']

    # PERIODO
    ini = datetime.datetime.strptime('10-02-2016', '%d-%m-%Y')
    fim = datetime.datetime.strptime('10-02-2017', '%d-%m-%Y')
    # CLASS IMPORT
    imp_b = importa_base(ini, fim, shares_tickers, index_tickers)
    ## IMPORT PRECOS
    df_price = imp_b.importa_precos()
    ## IMPORT INDICES
    df_indicadores = imp_b.importa_indicadores()
    ## IMPORT INDEX
    df_indexes = imp_b.importa_index()

    # PCT
    lista = [0.5, 0.5]

    # BACKTEST
    backtest(df_price, df_indexes, lista)