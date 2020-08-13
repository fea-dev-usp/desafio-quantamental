import numpy as np
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta
import pyfolio as pf
# from pypfopt.efficient_frontier import EfficientFrontier
# from pypfopt import risk_models, expected_returns


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

class importa_base():
    def __init__(self, dt_ini, dt_fim, tickers=None, index=None, indicad_path='..\\base_de_dados\\fundamentos_limpo\\indicadores.h5', price_path='..\\base_de_dados\\precos_limpo\\precos.h5', index_path='..\\base_de_dados\\index_limpo\\index.h5'):
        self.dt_ini = dt_ini
        self.dt_fim = dt_fim
        self.tickers = list(tickers)
        self.index = index
        # PATH BASE INDICADORES FINANCEIROS
        self.indicadores_path = indicad_path
        # PATH BASE INDEX (IBOV, CDI, IGP-M, ...)
        self.index_path = index_path
        # PATH BASE ACOES
        self.price_path = price_path

    def fix_tickers(self):
        return list(set([x[:4] for x in self.tickers]))

    def dict_x(self, tickers, path):
        dict_x = {}
        for t in tickers:
            dict_x[t] = pd.read_hdf(path, t)

        return dict_x

    def importa_precos(self):
        # DICT COM AS DF DOS PRECO HIST DOS TICKERS
        dict_prices = self.dict_x(self.tickers, self.price_path)
        # DICT COM AS DFS COM DEFINICOES IMPOSTA PELO USUARIO
        dict_limpa = {}
        # LIST COM AS ACOES Q N POSSUEM PRECO NO PERIODO
        list_priceless = []
        # COLUNAS DF PRICE
        cols = self.tickers

        # LIMPA DFS
        for name in dict_prices.keys():
            # print(name)
            # dict_limpa[name] = dict_prices[name]['preco'][self.dt_ini:self.dt_fim].to_frame().copy()
            x = dict_prices[name].loc[dict_prices[name].index <= self.dt_fim, 'preco'].to_frame().copy()
            dict_limpa[name] = x.loc[x.index >= self.dt_ini, 'preco'].to_frame().copy()
            # VERIFICA SE A ACAO EXISTE NESSE PERIODO
            if len(dict_limpa[name]) == 0:
                list_priceless.append(name)
                del dict_limpa[name]
                cols.remove(name)

        # JUNTA DFS EM UMA UNICA
        df_preco = pd.concat(dict_limpa.values(), axis=1)
        df_preco.columns = cols

        # PRINT DFS SEM PRECO
        if len(list_priceless) == 0:
            print('\033[94m' + 'Prices: Success!' + '\x1b[0m')
        else:
            print('\033[93m' + 'As acoes ', list_priceless, ' nao possuem preco nesse periodo')
        return df_preco

    def importa_index(self):
        # DICT COM AS DF DOS INDEX
        dict_index = self.dict_x(self.index, self.index_path)
        # DICT COM AS DFS COM DEFINICOES IMPOSTA PELO USUARIO
        dict_limpa = {}
        # LIST COM AS ACOES Q N POSSUEM PRECO NO PERIODO
        list_priceless = []
        # COLUNAS DF PRICE
        cols = self.index

        # LIMPA DFS
        for name in dict_index.keys():
            # ARRUMA INDEX
            dict_index[name].index = list(dict_index[name]['data'])
            # dict_limpa[name] = dict_prices[name]['index'][self.dt_ini:self.dt_fim].to_frame().copy()
            x = dict_index[name].loc[dict_index[name].index <= self.dt_fim.date(), 'valor'].to_frame().copy()
            dict_limpa[name] = x.loc[x.index >= self.dt_ini.date(), 'valor'].to_frame().copy()
            # VERIFICA SE A ACAO EXISTE NESSE PERIODO
            if len(dict_limpa[name]) == 0:
                list_priceless.append(name)
                del dict_limpa[name]
                cols.remove(name)

        # JUNTA DFS EM UMA UNICA
        df_index = pd.concat(dict_limpa.values(), axis=1)
        df_index.columns = cols

        # PRINT DFS SEM PRECO
        if len(list_priceless) == 0:
            print('\033[94m' + 'Index: Success!' + '\x1b[0m')
        else:
            print('\033[93m' + 'Os index ', list_priceless, ' nao possuem valores nesse periodo')
        return df_index

    def importa_indicadores(self):
        # ARRUMA TICKERS
        t = self.fix_tickers()
        # DICT COM AS DF DOS PRECO HIST DOS TICKERS
        dict_ind = self.dict_x(t, self.indicadores_path)
        # DICT COM AS DFS COM DEFINICOES IMPOSTA PELO USUARIO
        dict_limpa = {}
        # LIST COM AS ACOES Q N POSSUEM PRECO NO PERIODO
        list_priceless = []
        # NAMES
        names = list(dict_ind.keys())

        # LIMPA DFS
        for name in names:
            # print(name)
            # if name == 'SBSP':
            #     print('paraa')
            x = dict_ind[name].loc[dict_ind[name].index >= self.dt_ini.date()].copy()
            dict_limpa[name] = x.loc[x.index <= self.dt_fim.date()].copy()
            # VERIFICA SE A ACAO EXISTE NESSE PERIODO
            if len(dict_limpa[name]) == 0:
                list_priceless.append(name)
                del dict_limpa[name]
                # names.remove(name)

        # JUNTA DFS EM UMA UNICA
        df_ind = pd.concat(dict_limpa.values(), axis=1)
        ## REMOVE TIKERS DE NAMES
        [names.remove(x) for x in list_priceless]
        ## SUB INDEX
        sub_index = ['roa', 'fco', 'lc', 'alavancagem', 'shares', 'ga', 'margem_bruta']
        ## MULTIINDEX
        index = [(name, i) for name in names for i in sub_index]
        multiindex = pd.MultiIndex.from_tuples(index)
        df_ind.columns = multiindex

        # PRINT DFS SEM PRECO
        if len(list_priceless) == 0:
            print('\033[94m' + 'Indicadores: Success!' + '\x1b[0m')
        else:
            print('\033[93m' + 'As acoes ', list_priceless, ' nao possuem indicadores nesse periodo')

        return df_ind

class EVA:
    def __init__(self, series_tickers, first_period, index=['IBOV']):
        """

        :param series_tickers: pandas series, onde o index são os periodos da frequencia da estrategia,
        e os valores sao listas com todos os ticker das acoes que devem ser levadas em conta no periodo
        """
        self.series_tickers = series_tickers
        # LISTA C TODOS OS TICKERS
        self.all_tickers = set()
        [self.all_tickers.update(t) for t in self.series_tickers]
        # DATA INICIO
        self.dt_ini = first_period
        # BENCHMARK
        self.index = index
        # SERIES RETORNO ACOES
        self.sr_acoes = pd.Series(np.nan).reindex([self.dt_ini])
        # SERIES RETORNO BENCHMARK
        self.sr_ibov = pd.Series(np.nan).reindex([self.dt_ini])


    def run(self):
        # DATA FIM
        dt_fim = self.dt_ini + relativedelta(months=+3)
        # LOOPING PELOS TICKERS DE CADA PERIODO
        for p_tickers in self.series_tickers:
            # IMPORTA BASE
            imp_b = importa_base(self.dt_ini, dt_fim, tickers=p_tickers, index=self.index)
            ## PRECOS
            df_precos = imp_b.importa_precos()
            ## IBOV
            df_ibov = imp_b.importa_index()

            # PIOTROSKI
            ## INDICADORES FINANCEIROS
            ### DATA INI E FIM PIOTROSKI
            dt_fim_p = self.dt_ini - datetime.timedelta(days=1)
            imp_b.dt_fim = dt_fim_p
            dt_ini_p = dt_fim_p - relativedelta(months=+3) - datetime.timedelta(days=1)
            imp_b.dt_ini = dt_ini_p
            ### DF INDICADORES
            df_indicadores = imp_b.importa_indicadores()
            ## DF PIOTROSKI
            df_piotroski = f_score_piotroski(df_indicadores)
            ## TICKERS FILTRO
            arruma_t = list(df_piotroski.iloc[1][df_piotroski.iloc[1] >= 5].index)
            tickers_p = [x for x in df_precos.columns if x[:4] in arruma_t]
            ## FILTRA DF
            df_precos_p = df_precos[tickers_p].copy()

            # BACKTEST
            ## LISTA PORCENTAGEM ALOCACAO
            ### DF PRECOS MTZ
            # imp_b.tickers = tickers_p
            # df_precos_mtz = imp_b.importa_precos()
            # mtz = markowitz(df_precos_mtz)
            # pct = list(mtz.max_sharpe().values())
            pct = list(np.random.rand(len(df_precos_p.columns)))

            carteira, carteira_ibov = backtest(df_precos_p, df_ibov, pct)

            ## ADD A SERIES ACOES
            if np.isnan(self.sr_acoes[-1]):
                # ADD RETORNO
                self.sr_acoes = self.sr_acoes.append(carteira['retorno'].iloc[1:])
            else:
                # RETORNO MEDIO
                r_medio = pd.Series((self.sr_acoes[-1] + carteira['retorno'].iloc[1])/2, index=[carteira['retorno'].index[0]])
                self.sr_acoes = self.sr_acoes.append(r_medio)
                # ADD RETORNO
                self.sr_acoes = self.sr_acoes.append(carteira['retorno'].iloc[1:])
            ## ADD A SERIES IBOV
            if np.isnan(self.sr_ibov[-1]):
                # ADD RETORNO
                self.sr_ibov = self.sr_ibov.append(carteira_ibov['retorno'].iloc[1:])
            else:
                # RETORNO MEDIO
                r_medio = pd.Series((self.sr_ibov[-1] + carteira_ibov['retorno'].iloc[1]) / 2,
                                    index=[carteira_ibov['retorno'].index[0]])
                self.sr_ibov = self.sr_ibov.append(r_medio)
                # ADD RETORNO
                self.sr_ibov = self.sr_ibov.append(carteira_ibov['retorno'].iloc[1:])

            # ARRUMA DATA INI
            self.dt_ini = dt_fim + datetime.timedelta(days=1)
            dt_fim = dt_fim + relativedelta(months=+3)

        # CALCULA RETORNO
        ## ARRUMA INDE IBOV
        index_ibov = [pd.Timestamp(x) for x in self.sr_ibov.index]
        self.sr_ibov.reindex(index_ibov)
        self.sr_ibov.index = index_ibov
        ### PYFOLIO
        pf.create_full_tear_sheet(self.sr_acoes, benchmark_rets=self.sr_ibov)


def main():
    # DATA INI
    first_period = datetime.datetime.strptime('01-04-2016', '%d-%m-%Y')
    # SERIES TICKERS
    ## TICKERS
    tickers = [
        'ABEV3', 'AZUL4', 'B3SA3', 'BBAS3', 'BBDC3', 'BBDC4', 'BBSE3', 'BEEF3', 'BPAC11', 'BRAP4', 'BRDT3', 'TAEE11',
        'BRKM5', 'BRML3', 'BTOW3', 'CCRO3', 'CIEL3', 'CMIG4', 'COGN3', 'CPFE3', 'CRFB3', 'CSNA3', 'CVCB3',
        'CYRE3', 'ECOR3', 'ELET3', 'ELET6', 'EMBR3', 'ENBR3', 'ENGI11', 'EQTL3', 'FLRY3', 'GGBR4', 'GNDI3', 'SUZB3',
        'GOAU4', 'GOLL4', 'HAPV3', 'HGTX3', 'HYPE3', 'IGTA3', 'IRBR3', 'ITSA4', 'ITUB4', 'JBSS3', 'KLBN11', 'LAME4',
        'LREN3', 'MGLU3', 'MRFG3', 'MRVE3', 'MULT3', 'NTCO3', 'PCAR3', 'PETR3', 'PETR4', 'QUAL3', 'RADL3', 'RAIL3',
        'RENT3', 'SANB11', 'SBSP3', 'SULA11'
    ]
    ## NUMBER OF PERIODS
    periods = 12
    ## SERIES
    series_tickers = pd.Series([tickers for x in range(periods)])

    # RUN STRATEGY
    eva = EVA(series_tickers, first_period)
    eva.run()


if __name__ == '__main__':
    main()

    p_2011 = ['TIET3', 'AEDU3', 'BICB3', 'BBDC3', 'BBAS3', 'BRKM3', 'BRFS3', 'CMIG3', 'CESP3', 'COCE3', 'CSMG3', 'CPLE3',
            'CPFE3', 'DURA3', 'ELET3', 'ELPL3', 'EMBR3', 'ENBR3', 'EVEN3', 'FIBR3', 'GGBR3', 'GOAU3', 'ROMI3', 'ITSA3',
            'ITUB3', 'LIGH3', 'NATU3', 'RDCD3', 'SBSP3', 'SANB3', 'SULA3', 'SUZB3', 'TMAR3', 'TCSL4', 'EGIE3', 'UGPA3',
            'VALE3', 'VIVT4']
    p_2012 = ['TIET3', 'AEDU3', 'BICB3', 'BBDC3', 'BBAS3', 'BRKM3', 'BRFS3', 'CCRO3', 'CMIG3', 'CESP3', 'COCE3', 'CSMG3',
            'CPLE3', 'CPFE3', 'DURA3', 'ECOR3', 'ELET3', 'ELPL3', 'EMBR3', 'ENBR3', 'EVEN3', 'FIBR3', 'GGBR3', 'GOAU3',
            'ITSA3', 'ITUB3', 'LIGH3', 'NATU3', 'RDCD3', 'SBSP3', 'SANB3', 'SULA3', 'SUZB3', 'TMAR3', 'TCSL4', 'EGIE3',
            'UGPA3', 'VALE3']
    p_2013 = ['TIET3', 'BICB3', 'BBDC3', 'BBAS3', 'BRKM3', 'BRFS3', 'CCRO3', 'CMIG3', 'CESP3', 'COCE3', 'CSMG3', 'CPLE3',
            'CPFE3', 'DURA3', 'ECOR3', 'ELET3', 'ENBR3', 'ELPL3', 'EVEN3', 'FIBR3', 'GGBR3', 'GOAU3', 'ITSA3', 'ITUB3',
            'LIGH3', 'NATU3', 'OIBR3', 'SBSP3', 'SANB3', 'SULA3', 'SUZB3', 'VIVT3', 'TCSL4', 'EGIE3', 'UGPA3', 'VALE3',
            'WEGE3']
    p_2014 = ['TIET3', 'BICB3', 'BBDC3', 'BBAS3', 'BRKM3', 'BRFS3', 'CCRO3', 'CMIG3', 'CESP3', 'COCE3', 'CSMG3', 'CPLE3',
            'CPFE3', 'DURA3', 'ECOR3', 'ELET3', 'ENBR3', 'ELPL3', 'EMBR3', 'EVEN3', 'FIBR3', 'FLRY3', 'GGBR3', 'ITSA3',
            'ITUB3', 'KLBN3', 'LIGH3', 'GOAU3', 'NATU3', 'OIBR3', 'SBSP3', 'SANB3', 'SULA3', 'SUZB3', 'VIVT3', 'TCSL4',
            'EGIE3', 'VALE3', 'WEGE3']
    p_2015 = ['TIET3', 'BTOW3', 'BICB3', 'BBDC3', 'BBAS3', 'BRKM3', 'BRFS3', 'CCRO3', 'CMIG3', 'CIEL3', 'COCE3', 'CPLE3',
            'CPFE3', 'DURA3', 'ECOR3', 'ELET3', 'ENBR3', 'ELPL3', 'EMBR3', 'EVEN3', 'FIBR3', 'FLRY3', 'GGBR3', 'ITSA3',
            'ITUB3', 'JSLG3', 'KLBN3', 'LIGH3', 'GOAU3', 'LAME3', 'LREN3', 'NATU3', 'SBSP3', 'SANB3', 'SULA3', 'SUZB3',
            'VIVT3', 'TCSL4', 'EGIE3', 'VALE3', 'WEGE3']
    p_2016 = ['TIET3', 'BTOW3', 'BBDC3', 'BBAS3', 'BRKM3', 'BRFS3', 'CCRO3', 'CMIG3', 'CESP3', 'CIEL3', 'CPLE3', 'CPFE3',
            'DURA3', 'ECOR3', 'ELET3', 'ENBR3', 'ELPL3', 'EMBR3', 'EVEN3', 'FIBR3', 'FLRY3', 'ITSA3', 'ITUB3', 'KLBN3',
            'LIGH3', 'LAME3', 'LREN3', 'NATU3', 'OIBR3', 'SANB3', 'SULA3', 'SUZB3', 'VIVT3', 'TCSL4', 'EGIE3', 'WEGE3']
    p_2017 = ['TIET3', 'BTOW3', 'BBDC3', 'BBAS3', 'BRKM3', 'BRFS3', 'CCRO3', 'CLSC3', 'CMIG3', 'CIEL3', 'CPLE3', 'CPFE3',
            'DURA3', 'ECOR3', 'ELET3', 'ENBR3', 'ELPL3', 'EMBR3', 'EGIE3', 'FIBR3', 'FLRY3', 'ITSA3', 'ITUB3', 'KLBN3',
            'LIGH3', 'LAME3', 'LREN3', 'MRVE3', 'NATU3', 'SANB3', 'SULA3', 'VIVT3', 'TCSL4', 'WEGE3']
    p_2018 = ['TIET3', 'BTOW3', 'BBDC3', 'BBAS3', 'BRKM3', 'CCRO3', 'CLSC3', 'CMIG3', 'CIEL3', 'CPLE3', 'CPFE3', 'DURA3',
            'ECOR3', 'ELET3', 'ENBR3', 'ELPL3', 'EGIE3', 'FIBR3', 'FLRY3', 'ITSA3', 'ITUB3', 'KLBN3', 'LIGH3', 'LAME3',
            'LREN3', 'MRVE3', 'NATU3', 'SANB3', 'VIVT3', 'TCSL4', 'WEGE3']
    p_2019 = ['TIET3', 'BTOW3', 'BBDC3', 'BBAS3', 'BRKM3', 'CCRO3', 'CMIG3', 'CIEL3', 'CPLE3', 'DURA3', 'ECOR3', 'ELET3',
            'ENBR3', 'EGIE3', 'FLRY3', 'ITSA3', 'ITUB3', 'KLBN3', 'LIGH3', 'LAME3', 'LREN3', 'MRVE3', 'NATU3', 'SANB3',
            'VIVT3', 'TCSL4', 'WEGE3']