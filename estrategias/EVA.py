from backtest import backtest
from piotroski import f_score_piotroski
import numpy as np
from importa_base import importa_base
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta
import pyfolio as pf

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