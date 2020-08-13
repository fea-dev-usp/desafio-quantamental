import pandas as pd
import datetime

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


def main():
    # TICKERS / INDEX
    ## TICKERS FALTANDO
    # missing_tickers = ['BRFS3', 'EGIE3', 'CSAN3']
    tickers = [
        'ABEV3', 'AZUL4', 'B3SA3', 'BBAS3', 'BBDC3', 'BBDC4', 'BBSE3', 'BEEF3', 'BPAC11', 'BRAP4', 'BRDT3',
        'BRKM5', 'BRML3', 'BTOW3', 'CCRO3', 'CIEL3', 'CMIG4', 'COGN3', 'CPFE3', 'CRFB3', 'CSNA3', 'CVCB3',
        'CYRE3', 'ECOR3', 'ELET3', 'ELET6', 'EMBR3', 'ENBR3', 'ENGI11', 'EQTL3', 'FLRY3', 'GGBR4', 'GNDI3',
        'GOAU4', 'GOLL4', 'HAPV3', 'HGTX3', 'HYPE3', 'IGTA3', 'IRBR3', 'ITSA4', 'ITUB4', 'JBSS3', 'KLBN11', 'LAME4',
        'LREN3', 'MGLU3', 'MRFG3', 'MRVE3', 'MULT3', 'NTCO3', 'PCAR3', 'PETR3', 'PETR4', 'QUAL3', 'RADL3', 'RAIL3',
        'RENT3', 'SANB11', 'SBSP3', 'SULA11', 'SUZB3', 'TAEE11'
    ]
    # tickers = ['ABEV3', 'AZUL4', 'B3SA3']
    index = ['IBOV']
    # PERIODO
    ini = datetime.datetime.strptime('01-02-2010', '%d-%m-%Y')
    fim = datetime.datetime.strptime('10-02-2017', '%d-%m-%Y')
    # CLASS IMPORT
    imp_b = importa_base(ini, fim, tickers, index)
    ## IMPORT PRECOS
    price = imp_b.importa_precos()
    ## IMPORT INDICES
    indices = imp_b.importa_indicadores()
    ## IMPORT INDEX
    indexes = imp_b.importa_index()

    return price, indices, indexes
if __name__ == '__main__':
    price, ind, index = main()
    print('__________**ACABOU**__________')