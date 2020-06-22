# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 13:20:17 2020

@author: JOAO VICTOR
"""
import yfinance as yf
import pandas_datareader.data as web
import pandas as pd
import pyfolio as pf
import warnings
import fundamentos as ftos
from alpha_vantage.timeseries import TimeSeries

ALPHAVANTAGE_API_KEY = 'LR7S2ABGWS1U7HLY'
ts = TimeSeries(key=ALPHAVANTAGE_API_KEY)
dados = ts.get_daily(symbol = '^BVSP')

warnings.filterwarnings('ignore')
yf.pdr_override()

def result_backtest_ibov(stock, datainicial, datafinal):
    ibov = ['^BVSP']
    dados_yahoo = web.get_data_yahoo(stock, start='{}'.format(datainicial), end='{}'.format(datafinal))['Adj Close']
    dados_ibov = web.get_data_yahoo(ibov, start='{}'.format(datainicial), end='{}'.format(datafinal))['Adj Close']

    bench = dados_ibov.pct_change()

    bench_acumulado = (1+bench).cumprod()
    bench_acumulado.iloc[0] = 1

    carteira_ibov = 10000*bench_acumulado
    carteira_ibov['retorno'] = carteira_ibov.pct_change()

    retorno = dados_yahoo.pct_change()

    retorno_acumulado = (1 + retorno).cumprod()
    retorno_acumulado.iloc[0] = 1

    carteira = 10000*retorno_acumulado
    carteira['saldo'] = carteira.sum(axis=1)
    carteira['retorno'] = carteira['saldo'].pct_change()

    return pf.create_full_tear_sheet(carteira['retorno'], benchmark_rets=carteira_ibov['retorno'])

ticker2016 = ['TIET11.SA','BTOW3.SA','BBAS3.SA', 'BBDC3.SA', 'BRKM3.SA', 'BRFS3.SA', 'CCRO3.SA', 'CMIG3.SA',
          'CESP3.SA', 'CIEL3.SA', 'CPLE3.SA', 'CPFE3.SA', 'DTEX3.SA', 'ECOR3.SA', 'ENBR3.SA', 'ELET3.SA',
          'EMBR3.SA', 'EVEN3.SA', 'SUZB3.SA', 'FLRY3.SA', 'ITSA4.SA', 'ITUB3.SA', 'KLBN11.SA',
          'LAME4.SA', 'LIGT3.SA', 'OIBR4.SA', 'LREN3.SA', 'SANB11.SA', 'SULA11.SA', 'VIVT4.SA',
          'TIMP3.SA', 'EGIE3.SA', 'WEGE3.SA' ]
ticker2017 = ['TIET11.SA', 'BTOW2.SA', 'BBDC3.SA', 'BBAS3.SA', 'BRKM3.SA', 'BRFS3.SA', 'CCRO3.SA',
              'CMIG3.SA', 'CLSC3.SA', 'CIEL3.SA', 'CPLE3.SA', 'PALF11.SA', 'DTEX3.SA', 'ECOR3.SA',
              'ENBR2.SA', 'ELET3.SA', 'ELPL3.SA', 'EMBR3', 'EGIE3.SA', 'FIBR3.SA', 'FLRY3.SA',
              'ITSA3.SA', 'ITUB3.SA', 'KLBN11.SA', 'LIGH3.SA', 'LAME3.SA', 'LREN3.SA', 'MRVE3.SA',
              'NATU3.SA', 'SANB11.SA', 'SULA11.SA', 'TEFC11.SA', 'TCSL4.SA', 'WEGE3.SA']
ticker2018 = []
result_backtest_ibov(ticker2016, '2016-01-01', '2017-01-01')
result_backtest_ibov(ticker2017, '2017-01-01', '2018-01-01')
df = ftos.get_tickers()