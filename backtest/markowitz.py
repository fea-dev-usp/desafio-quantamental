import pandas as pd
import numpy as np
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models, expected_returns

class Markowitz():
    def __init__(self, df):
        self.df = df
        
        self.mu = expected_returns.mean_historical_return(df)
        
        self.S = risk_models.sample_cov(df)
        
        self.ef = EfficientFrontier(self.mu, self.S)
        
    def max_sharpe(self):
        '''Essa função retorna os pesos dos ativos de tal modo que maximiza o sharpe da carteira'''
        self.ef.max_sharpe()
        cleaned_weights = self.ef.clean_weights()
        return cleaned_weights

### EXEMPLO DE USO ###

from pandas_datareader import data as web
from datetime import datetime
import matplotlib.pyplot as plt

tickers = ['VVAR3.SA', 'MGLU3.SA', 'CSAN3.SA']

inicio = '2018-01-01'
fim = '2019-12-01'

df = web.DataReader(tickers, data_source = 'yahoo', start = inicio, end = fim)

df = df['Adj Close']

markowitz = Markowitz(df)

print(markowitz.max_sharpe())
