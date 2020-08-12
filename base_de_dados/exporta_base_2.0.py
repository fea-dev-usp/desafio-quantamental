import numpy as np
import pandas as pd
import datetime
from os import listdir, remove
from os.path import isfile, join

class exporta_base():
    def __init__(self, fund_path_folder=None, price_path_folder=None, index_path_folder=None):
        self.price_path_folder = price_path_folder
        self.fund_path_folder = fund_path_folder
        self.index_path_folder = index_path_folder
        self.dict_dre = {}
        self.dict_bp = {}
        self.dict_dfc = {}
        self.dict_prices = {}
        self.dict_index = {}
        self.nomes = set()
        self.dict_indicadores = {}

    def printProgressBar(self, iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
            printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
        """
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
        # Print New Line on Complete
        if iteration == total:
            print()

    def index_already_exixt(self, ticker, base):
        """

        :param tickers:
        :param base: can be: 'BP', 'DRE, 'DFC', 'Price'
        :return: a list
        """

        # CHECK IN DEMOSNTRATIVOS (FUNDAMENTOS)
        if 'BP' == base:
            # LE AS BASES DE DADOS
            dre = pd.HDFStore('\\fundamentos_limpo\\dre.h5')
            # SET COM AS EMPRESAS QUE N ESTAO NA BASE
            dif_names = {ticker} if ticker not in dre else set()
            #CLOSE
            dre.close()

            return True if len(dif_names) == 0 else False

        # CHECK IN DFC
        elif 'DFC' == base:
            # LE A BASE DE DADOS
            dfc = pd.HDFStore('\\fundamentos_limpo\\dfc.h5')
            # SET COM AS EMPRESAS QUE N ESTAO NA BASE
            dif_names = {ticker} if ticker not in dfc else set()
            # CLOSE
            dfc.close()

            return True if len(dif_names) == 0 else False

        # CHECK IN DRE
        elif 'DRE' == base:
            # LE A BASE DE DADOS
            bp = pd.HDFStore('\\fundamentos_limpo\\bp.h5')
            # SET COM AS EMPRESAS QUE N ESTAO NA BASE
            dif_names = {ticker} if ticker not in bp else set()
            # CLOSE
            bp.close()

            return True if len(dif_names) == 0 else False

        # CHECK IN PRECOS
        elif 'Prices' == base:
            # LE AS BASES DE DADOS
            prices = pd.HDFStore('\\precos_limpo\\precos.h5')
            # SET COM AS EMPRESAS QUE N ESTAO NA BASE
            dif_names = {ticker} if ticker not in prices else set()
            # CLOSE
            prices.close()

            return True if len(dif_names) == 0 else False

            # CHECK IN PRECOS
        elif 'Index' == base:
            # LE AS BASES DE DADOS
            index = pd.HDFStore('\\index_limpo\\index.h5')
            # SET COM AS EMPRESAS QUE N ESTAO NA BASE
            dif_names = {ticker} if ticker not in index else set()
            # CLOSE
            index.close()

            return True if len(dif_names) == 0 else False

    def dfs_funds(self):
        # NOME DOS ARQUIVOS EXCEL
        files_names = [f for f in listdir(self.fund_path_folder) if isfile(join(self.fund_path_folder, f))]

        #CREATE A DICT OF DFs
        dict_f = {}
        l = 0
        for excel_p in files_names:
            x = pd.read_excel(self.fund_path_folder + str('\\') + excel_p, sheet_name=None)
            y = dict(zip(list(range(l,l+len(x))), list(x.values())))
            dict_f.update(y)
            l += len(x)

        return dict_f

    def nome_t_relat(self, df):
        empresa = list(df["Unnamed: 0"][3])
        name = df["Unnamed: 0"][3][empresa.index(':') + 1:[i for i, x in enumerate(empresa) if x == ")"][-1]][:4]
        # TIPO RELATORIO
        values = np.array(empresa)
        idx = np.where(values == '>')[0][-1]
        nome_demons_ori = df["Unnamed: 0"][3][idx + 2:]
        if nome_demons_ori == 'Income Statement':
            nome_demons = 'DRE'
        elif nome_demons_ori == 'Balance Sheet':
            nome_demons = 'BP'
        elif nome_demons_ori == 'Cash Flow':
            nome_demons = 'DFC'

        return name, nome_demons

    def muda_col(self, df, nome_demons):
        # LISTA NOME COLUNAS
        col_list = [x[-11:] for x in df.loc[[13]].values[0][1:]]
        col_list_dt = [nome_demons] + [datetime.datetime.strptime(x, '%b-%d-%Y').strftime('%d/%m/%Y') for x in col_list]

        # # MUDA NOME COLUNAS
        df.columns = col_list_dt

    def limpa_base_f(self):
        # DICT COM DFS
        dict_dfs = self.dfs_funds()

        # Initial call to print 0% progress
        l = len(dict_dfs.values())
        i = 0
        self.printProgressBar(0, l, prefix='Progress:', suffix='Complete', length=50)

        for df in dict_dfs.values():
            # NOME/ TIPO RELATORIO
            name, nome_demons = self.nome_t_relat(df)

            # VERIFICA SE AS EMPRESAS JA ESTPA NA BASE
            if self.index_already_exixt(name, nome_demons):
                continue

            # if name == 'BBAS':
            #     print('paraaa')

            # # REMOVE 'FISCAL YEAR CHANGE'
            nome_col = [x[-11:] for x in df.loc[[13]].values[0][1:]]
            indices = [i for i, x in enumerate(nome_col) if x == "Year\nChange"]
            col_drop = ['Unnamed: ' + str(x+1) for x in indices]
            df_new = df.drop(columns=col_drop).copy()

            # MUDA NOME COLUNAS
            self.muda_col(df_new, nome_demons)

            # REMOVE INFO EXTRA
            # # DROP PRIMEIRAS LINHAS DESNECESSARIAS
            df_new = df_new.drop(df.index[:16], axis='index')
            df_new = df_new.drop(df.index[-2:], axis='index')

            ## DROP LINHAS VAZIAS
            df_new = df_new[df_new[nome_demons].notna()]

            # LISTA NOME INDEX
            index = [x.lstrip(' ') for x in list(df_new[nome_demons])]
            df_new.index = index
            df_new = df_new.drop(columns=nome_demons)

            # NAN TO 0
            df_new = df_new.fillna(0)
            df_new = df_new.replace('-', 0)

            # REMOVE DUPLICATES OF INDEX
            df_new = df_new.loc[~df_new.index.duplicated(keep='first')]

            # ADD AO DICT DE DEMONSTRATIVOS
            if nome_demons == 'DRE':
                self.dict_dre[name] = df_new
            elif nome_demons == 'DFC':
                self.dict_dfc[name] = df_new
            elif nome_demons == 'BP':
                self.dict_bp[name] = df_new
            else:
                print(name)

            self.nomes.add(name)

            # Update Progress Bar
            self.printProgressBar(i + 1, l, prefix='Progress:', suffix='Complete', length=50)
            i += 1

        # CREATE A HDF5 FILE - BP
        for empresa in self.dict_bp.keys():
            self.dict_bp[empresa].to_hdf('..\\base_de_dados\\fundamentos_limpo\\bp.h5', key=empresa, mode='a')

        # CREATE A HDF5 FILE - DFC
        for empresa in self.dict_dfc.keys():
            self.dict_dfc[empresa].to_hdf('..\\base_de_dados\\fundamentos_limpo\\dfc.h5', key=empresa, mode='a')

        # CREATE A HDF5 FILE - DRE
        for empresa in self.dict_dre.keys():
            self.dict_dre[empresa].to_hdf('..\\base_de_dados\\fundamentos_limpo\\dre.h5', key=empresa, mode='a')

    def indicadores(self, atuliza_base=False):
        cols = ['roa', 'fco', 'lc', 'alavancagem', 'shares', 'ga', 'margem_bruta']
        # DICT C DFS
        dict_dfs = {}
        # EMPREAS
        dif_names = self.nomes

        # CRIA APENAS OS INDICADORES DAS EMPRESAS Q N ESTAO NA BASE
        if atuliza_base is False:
            # HDF FILE
            ind = pd.HDFStore('..\\base_de_dados\\fundamentos_limpo\\indicadores.h5')
            # LISTA COM AS EMPRESAS QUE N ESTAO NA BASE
            dif_names = [x for x in self.nomes if x not in ind]

        for nome in dif_names:
            print(nome)
            if nome == 'ABEV':
                print('paraa')
            # ROA = ATIVO TOTAL MEDIO/ LUCRO LIQUIDO
            ## ATIVO MEDIO
            ativo_total = self.dict_bp[nome].loc['Total Assets'].to_numpy().reshape(1, self.dict_bp[nome].loc['Total Assets'].count())
            ativo_total_1 = ativo_total[0][1:].reshape(1, len(ativo_total[0])-1)
            ativo_total_1[ativo_total_1 == 0] = 0.000000000000000000000000000000000000000001
            ativo_total_0 = ativo_total[0][:-1].reshape(1, len(ativo_total[0])-1)
            ativo_total_0[ativo_total_1 == 0] = 0.000000000000000000000000000000000000000001
            at_medio = np.divide(ativo_total_1 + ativo_total_0, 2)

            ## LUCRO LIQUIDO
            l_liquido = self.dict_dre[nome].loc['Net Income'].to_numpy()[1:].reshape(1, self.dict_dre[nome].loc['Net Income'].count()-1)
            l_liquido[l_liquido == 0] = 0.000000000000000000000000000000000000000001

            roa = np.divide(l_liquido, at_medio)
            roa = np.insert(roa, 0, 0).reshape(1,self.dict_dre[nome].loc['Net Income'].count())

            # FCO
            fco = self.dict_dfc[nome].loc['Cash from Ops.'].to_numpy().reshape(1, self.dict_dfc[nome].loc['Cash from Ops.'].count())

            # LC = AC/PC
            ## AT
            ac = self.dict_bp[nome].loc['Total Current Assets'].to_numpy().reshape(1, self.dict_bp[nome].loc['Total Current Assets'].count())
            ac[ac == 0] = 0.000000000000000000000000000000000000000001

            ## PC
            pc = self.dict_bp[nome].loc['Total Current Liabilities'].to_numpy().reshape(1, self.dict_bp[nome].loc['Total Current Liabilities'].count())
            pc[pc == 0] = 0.000000000000000000000000000000000000000001

            lc = np.divide(ac, pc)

            # ENDIVIDAMENTO: PC/ (PC + PNC)
            ## PNC
            pnc = self.dict_bp[nome].loc['Total Current Liabilities'].to_numpy().reshape(1, self.dict_bp[nome].loc[
                'Total Current Liabilities'].count())
            pnc[pnc == 0] = 0.000000000000000000000000000000000000000001

            ## PASSIVO TOTAL
            passivo_t = self.dict_bp[nome].loc['Total Liabilities'].to_numpy().reshape(1, self.dict_bp[nome].loc[
                'Total Liabilities'].count())
            passivo_t[passivo_t == 0] = 0.000000000000000000000000000000000000000001
            endividamento = pc / passivo_t

            # ALAVANCAGEM FINANCEIRA: LUCRO OPERACIONAL / (LUCRO OPERACIONAL - DESPESAS FINANCEIRAS)
            ## LUCRO OPERACIONAL: (RECEITA DE VENDAS - CUSTOS) / (DESPESAS OPERACIONAIS  + REC. FIN.)

            # QTDE ACOES
            shares = self.dict_bp[nome].loc['Total Shares Out. on Balance Sheet Date'].to_numpy().reshape(1, self.dict_bp[nome].loc['Total Shares Out. on Balance Sheet Date'].count())

            # MARGEM BRUTA: LUCRO BRUTO / RECEITA BRUTA
            ## RECEITA BRUTA
            receita = self.dict_dre[nome].loc['Total Revenue'].to_numpy().reshape(1, self.dict_dre[nome].loc['Total Revenue'].count())
            receita[receita == 0] = 0.000000000000000000000000000000000000000001
            ## LUCRO BRUTO
            lucro_bruto = self.dict_dre[nome].loc['Net Income'].to_numpy().reshape(1, self.dict_dre[nome].loc['Net Income'].count())
            margem_bruta = lucro_bruto / receita

            # GA = RECITA DE VENDAS LIQUIDA/ATIVO TOTAL MEDIO
            ## VENDAS LIQUIDAS
            vend_liq = self.dict_dre[nome].loc['Total Revenue'].to_numpy()[1:].reshape(1, self.dict_dre[nome].loc['Total Revenue'].count()-1)
            vend_liq[vend_liq == 0] = 0.000000000000000000000000000000000000000001

            ga = np.divide(vend_liq, at_medio)
            ga = np.insert(ga, 0, 0).reshape(1, self.dict_dre[nome].loc['Total Revenue'].count())

            # CREATE DF
            ## INDEX
            str_arrumadas = [x[:-2] if '.' in x else x for x in self.dict_bp[nome].columns]
            index = [datetime.datetime.strptime(x, '%d/%m/%Y').date() for x in str_arrumadas]
            df = pd.DataFrame(np.concatenate((roa.T, fco.T, lc.T, endividamento.T, shares.T, ga.T, margem_bruta.T), axis=1), columns=cols, index=index)
            # ADD DICT
            dict_dfs[nome] = df

        # CREATE A HDF5 FILE
        for empresa in dict_dfs.keys():
            dict_dfs[empresa].to_hdf('..\\base_de_dados\\fundamentos_limpo\\indicadores.h5', key=empresa, mode='a')

    def dfs_prices(self):
        # NOME DOS ARQUIVOS EXCEL
        files_names = [f for f in listdir(self.price_path_folder) if isfile(join(self.price_path_folder, f))]

        #CREATE A LIST OF DFs
        list_file = []
        for file in files_names:
            list_file.append(pd.read_excel(self.price_path_folder + str('\\') + file))

        return list_file

    def limpa_base_p(self):
        # CRIA DFS PARA CADA EMPRESA
        dfs_prices = self.dfs_prices()

        # Initial call to print 0% progress
        l = len(dfs_prices)
        i = 0
        self.printProgressBar(0, l, prefix='Progress:', suffix='Complete', length=50)

        # LIMPA OS DFS
        for df in dfs_prices:
            # NOME ACAO
            empresa = list(df["Unnamed: 1"][34])
            name = df["Unnamed: 1"][34][empresa.index(':') + 1:[i for i, x in enumerate(empresa) if x == ")"][-1]]

            # VERIFICA SE AS EMPRESAS JA ESTPA NA BASE
            if self.index_already_exixt(name, 'Prices'):
                continue

            # MUDA NOME COLUNAS
            cols = ['data', 'volume', 'preco']
            df.columns = cols

            # DROP LINHAS DESNECESSARIAS
            df = df.drop(df.index[:35], axis='index')

            # CORRIGE O FORMATO DAS DATAS; TO DATETIME
            df['data'] = [x.date() for x in df['data']]

            # ADICIONA DF AO DICIONARIO
            self.dict_prices[name] = df

            # Update Progress Bar
            self.printProgressBar(i + 1, l, prefix='Progress:', suffix='Complete', length=50)
            i += 1

        # CREATE A HDF5 FILE
        for empresa in self.dict_prices.keys():
            self.dict_prices[empresa].to_hdf('..\\base_de_dados\\precos_limpo\\precos.h5', key=empresa, mode='a')

    def dfs_index(self):
        # NOME DOS ARQUIVOS EXCEL
        files_names = [f for f in listdir(self.index_path_folder) if isfile(join(self.index_path_folder, f))]

        #CREATE A LIST OF DFs
        list_file = []
        for file in files_names:
            list_file.append(pd.read_excel(self.index_path_folder + str('\\') + file))

        return list_file

    def limpa_base_index(self):
        # CRIA DFS PARA CADA EMPRESA
        dfs_index = self.dfs_index()

        # Initial call to print 0% progress
        l = len(dfs_index)
        i = 0
        self.printProgressBar(0, l, prefix='Progress:', suffix='Complete', length=50)

        # LIMPA OS DFS
        for df in dfs_index:
            # NOME ACAO
            empresa = list(df["Unnamed: 1"][34])
            name = df["Unnamed: 1"][34][empresa.index('(') + 1:[i for i, x in enumerate(empresa) if x == ")"][-1]]

            # VERIFICA SE O INDEX JA ESTA NA BASE
            if self.index_already_exixt(name, 'Index'):
                continue

            # MUDA NOME COLUNAS
            cols = ['data', 'valor']
            df.columns = cols

            # DROP LINHAS DESNECESSARIAS
            df = df.drop(df.index[:35], axis='index')

            # CORRIGE O FORMATO DAS DATAS; TO DATETIME
            df['data'] = [x.date() for x in df['data']]

            # ADICIONA DF AO DICIONARIO
            self.dict_index[name] = df

            # Update Progress Bar
            self.printProgressBar(i + 1, l, prefix='Progress:', suffix='Complete', length=50)
            i += 1

        # CREATE A HDF5 FILE
        for empresa in self.dict_index.keys():
            self.dict_index[empresa].to_hdf('..\\base_de_dados\\index_limpo\\index.h5', key=empresa, mode='a')


def main():
    base_path = "\\fundamentos_sujos"
    price_path_folder = "\\precos_sujos"
    index_path_folder = "\\index_sujos"
    exp_b = exporta_base(base_path, price_path_folder=price_path_folder, index_path_folder=index_path_folder)

    tickers = [
        'ABEV3', 'AZUL4', 'B3SA3', 'BBAS3', 'BBDC3', 'BBDC4', 'BBSE3', 'BEEF3', 'BPAC11', 'BRAP4', 'BRDT3', 'BRFS3',
        'BRKM5', 'BRML3', 'BTOW3', 'CCRO3', 'CIEL3', 'CMIG4', 'COGN3', 'CPFE3', 'CRFB3', 'CSAN3', 'CSNA3', 'CVCB3',
        'CYRE3', 'ECOR3', 'EGIE3', 'ELET3', 'ELET6', 'EMBR3', 'ENBR3', 'ENGI11', 'EQTL3', 'FLRY3', 'GGBR4', 'GNDI3',
        'GOAU4', 'GOLL4', 'HAPV3', 'HGTX3', 'HYPE3', 'IGTA3', 'IRBR3', 'ITSA4', 'ITUB4', 'JBSS3', 'KLBN11', 'LAME4',
        'LREN3', 'MGLU3', 'MRFG3', 'MRVE3', 'MULT3', 'NTCO3', 'PCAR3', 'PETR3', 'PETR4', 'QUAL3', 'RADL3', 'RAIL3',
        'RENT3', 'SANB11', 'SBSP3', 'SULA11', 'SUZB3', 'TAEE11', 'OIBR4', 'ABEV3', 'AZUL4', 'B3SA3', 'BBAS3'
    ]

    # LIMPA E EXPORTA INDICADORES EMPRESAS
    # exp_b.limpa_base_f()
    exp_b.nomes = [x[:4] for x in tickers]
    exp_b.dict_bp = dict_x(exp_b.nomes, '../base_de_dados/fundamentos_limpo/bp.h5')
    exp_b.dict_dfc = dict_x(exp_b.nomes, '../base_de_dados/fundamentos_limpo/dfc.h5')
    exp_b.dict_dre = dict_x(exp_b.nomes, '../base_de_dados/fundamentos_limpo/dre.h5')
    # exp_b.nomes = list(exp_b.dict_bp.keys())

    exp_b.indicadores(True)

    # # LIMPA E EXPORTA PRECOS ACOES
    # exp_b.dfs_prices()
    # exp_b.limpa_base_p()

    # LIMPA E EXPORTA VALOR INDEX
    # exp_b.dfs_index()
    # exp_b.limpa_base_index()

def excel_to_hdf():
    # # DICT PRECO
    # dict_prices = pd.read_excel('..\\base_de_dados\\precos_limpo\\precos.xlsx', sheet_name=None, index_col=0)
    # # CREATE A HDF5 FILE - PRECO
    # for empresa in dict_prices.keys():
    #     dict_prices[empresa].to_hdf('..\\base_de_dados\\precos_limpo\\precos.h5', key=empresa, mode='a')

    # DICT INDICADORES
    dict_ind = pd.read_excel('..\\base_de_dados\\fundamentos_limpo\\indicadores.xlsx', sheet_name=None, index_col=0)
    # CREATE A HDF5 FILE - INDICADORES
    for empresa in dict_ind.keys():
        dict_ind[empresa].to_hdf('..\\base_de_dados\\fundamentos_limpo\\indicadores.h5', key=empresa, mode='a')

    # DICT DFC
    dict_ind = pd.read_excel('..\\base_de_dados\\fundamentos_limpo\\dfc.xlsx', sheet_name=None, index_col=0)
    # CREATE A HDF5 FILE - DFC
    for empresa in dict_ind.keys():
        dict_ind[empresa].to_hdf('..\\base_de_dados\\fundamentos_limpo\\dfc.h5', key=empresa, mode='a')

    # DICT DRE
    dict_ind = pd.read_excel('..\\base_de_dados\\fundamentos_limpo\\dre.xlsx', sheet_name=None, index_col=0)
    # CREATE A HDF5 FILE - DRE
    for empresa in dict_ind.keys():
        dict_ind[empresa].to_hdf('..\\base_de_dados\\fundamentos_limpo\\dre.h5', key=empresa, mode='a')

    # DICT BP
    dict_ind = pd.read_excel('..\\base_de_dados\\fundamentos_limpo\\bp.xlsx', sheet_name=None, index_col=0)
    # CREATE A HDF5 FILE - BP
    for empresa in dict_ind.keys():
        dict_ind[empresa].to_hdf('..\\base_de_dados\\fundamentos_limpo\\bp.h5', key=empresa, mode='a')


def dict_x(tickers, path):
    dict_x = {}
    for t in tickers:
        dict_x[t] = pd.read_hdf(path, t)

    return dict_x

if __name__ == '__main__':
    main()
    # excel_to_hdf()