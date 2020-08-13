# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 14:25:20 2020

@author: JOAO VICTOR
"""

# import fundamentos as ftos
import pandas as pd
from importa_base import importa_base
import datetime
import numpy as np


def f_score_piotroski(df_ticker, score_unit=1):
    # VALOR SCORE
    scr = score_unit
    # DICT SCORES
    scores = {}

    #LOOPING IN TICKERS
    for ticker, new_df in df_ticker.groupby(axis=1, level=0):
        # LEN ROW
        tamanho = len(new_df[ticker]['roa'])
        # SCORE
        score = np.zeros((1, tamanho)).reshape(1,tamanho)

        # ROA corrente positivo, score +1
        score += new_df[ticker]['roa'].apply(lambda x: scr if x > 0 else 0).to_numpy().reshape(1, tamanho)

        # FCO positivo, score +1
        score += new_df[ticker]['fco'].apply(lambda x: scr if x > 0 else 0).to_numpy().reshape(1, tamanho)

        # ROA corrente maior que ROA passado, score +1
        score += new_df[ticker]['roa'].pct_change().apply(lambda x: scr if x > 0 else 0).to_numpy().reshape(1, tamanho)

        # #FCO corrente maior que Lucro Líquido corrente, score +1
        # if df['Fluxo de Caixa'].loc[current_year].loc['FCO'] > current_ll:
        #     score += 1

        #Alavancagem Passado maior que Alavancagem presente, score +1
        score += new_df[ticker]['alavancagem'].pct_change().apply(lambda x: scr if x > 0 else 0).to_numpy().reshape(1, tamanho)

        #Liquidez Corrente maior que Liquidez passada, score +1
        score += new_df[ticker]['lc'].pct_change().apply(lambda x: scr if x > 0 else 0).to_numpy().reshape(1, tamanho)

        #Quantidade de Ações permaneceu igual, score +1
        score += new_df[ticker]['shares'].pct_change().apply(lambda x: scr if x == 0 else 0).to_numpy().reshape(1, tamanho)

        #Margem Bruta corrente maior que Margem Bruta passada, score +1
        score += new_df[ticker]['margem_bruta'].pct_change().apply(lambda x: scr if x == 0 else 0).to_numpy().reshape(1, tamanho)

        #Giro de Ativo Corrente maior que Giro de Ativo Passado, score +1
        score += new_df[ticker]['ga'].pct_change().apply(lambda x: scr if x == 0 else 0).to_numpy().reshape(1, tamanho)

        # ADD TO DICT
        scores[ticker] = score[0]

    # CREATE DF SCORE
    ## INDEX
    index = df_ticker.index
    ## DF
    df_score = pd.DataFrame.from_dict(scores)
    df_score.index = index

    return df_score

if __name__ == '__main__':
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

    # SOCRE UNIT
    score_unit = 1

    test = f_score_piotroski(df_indicadores, score_unit)
