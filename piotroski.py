# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 14:25:20 2020

@author: JOAO VICTOR
"""

import fundamentos as ftos
import pandas as pd

#Parâmetros
ticker = 'PETR4'
current_year = '2009'
last_year = '2008'

def f_score_piotroski(ticker, last_year, current_year):
    score = 0
    df = ftos.get_fundamentos(ticker)

#calculando ROA corrente
    current_ll = df['Resultados'].loc[current_year].loc['Lucro Líquido']
    current_at = df['Patrimônio'].loc[current_year].loc['Ativo Total']
    current_roa = current_ll/current_at

#ROA corrente positivo, score +1
    if current_roa > 0:
        score += 1

#FCO positivo, score +1
    if df['Fluxo de Caixa'].loc[current_year].loc['FCO'] > 0:
        score += 1

#Calculando ROA passado
    last_ll = df['Resultados'].loc[last_year].loc['Lucro Líquido']
    last_at = df['Patrimônio'].loc[last_year].loc['Ativo Total']
    last_roa = last_ll/last_at

#ROA corrente maior que ROA passado, score +1
    if current_roa > last_roa:
        score += 1

#FCO corrente maior que Lucro Líquido corrente, score +1
    if df['Fluxo de Caixa'].loc[current_year].loc['FCO'] > current_ll:
        score += 1

#Calculando Alavangagem Passada e Corrente
    last_divida = df['Dívida'].loc[last_year].loc['Dívida Líquida']
    current_divida = df['Dívida'].loc[current_year].loc['Dívida Líquida']

    last_leverage = last_divida / last_at
    current_leverage = current_divida / current_at

#Alavancagem Passado maior que Alavancagem presente, score +1
    if last_leverage > current_leverage:
        score += 1

#calculando Liquidez Corrente e Passada
    last_pc = df['Liquidez e Solvência'].loc[last_year].loc['Passivo Circulante']
    current_pc = df['Liquidez e Solvência'].loc[current_year].loc['Passivo Circulante']

    last_ac = df['Liquidez e Solvência'].loc[last_year].loc['Ativo Circulante']
    current_ac = df['Liquidez e Solvência'].loc[current_year].loc['Ativo Circulante']

    last_lc = last_ac / last_pc
    current_lc = current_ac / current_pc

#Liquidez Corrente maior que Liquidez passada, score +1
    if current_lc > last_lc:
        score += 1

#Quantidade de Ações permaneceu igual, score +1
    if df['Mercado'].loc[current_year].loc['Quantidade de Ações ON'] ==  df['Mercado'].loc[last_year].loc['Quantidade de Ações ON']:
        score += 1

#Margem Bruta corrente maior que Margem Bruta passada, score +1
    if df['Resultados'].loc[current_year].loc['Margem Bruta'] > df['Resultados'].loc[last_year].loc['Margem Bruta']:
        score += 1

#Calculando Giro de Ativo Passado e Corrente
    last_average_at = last_at / 12
    current_average_at = current_at / 12
    last_giro_ativo = df['Resultados'].loc[last_year].loc['Receita Líquida'] / last_average_at
    current_giro_ativo = df['Resultados'].loc[current_year].loc['Receita Líquida'] / current_average_at

#Giro de Ativo Corrente maior que Giro de Ativo Passado, score +1
    if current_giro_ativo > last_giro_ativo:
        score += 1
    return score

test = f_score_piotroski(ticker, last_year, current_year)