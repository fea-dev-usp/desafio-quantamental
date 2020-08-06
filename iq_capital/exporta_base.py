import numpy as np
import pandas as pd
import datetime
from os import listdir, remove
from os.path import isfile, join

class exporta_base():
    def __init__(self, fund_path_folder=None, price_path_folder=None):
        self.price_path_folder = price_path_folder
        self.fund_path_folder = fund_path_folder
        self.dict_dre = {}
        self.dict_bp = {}
        self.dict_dfc = {}
        self.dict_prices = {}
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

        dict_dfs = self.dfs_funds()
        # Initial call to print 0% progress
        l = len(dict_dfs.values())
        i = 0
        self.printProgressBar(0, l, prefix='Progress:', suffix='Complete', length=50)

        for df in dict_dfs.values():
            # NOME/ TIPO RELATORIO
            name, nome_demons = self.nome_t_relat(df)

            if name in self.nomes:
                pass

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

        # CREATE A EXCEL FILE - BP
        with pd.ExcelWriter('..\\iq_capital\\fundamentos_limpo\\bp.xlsx') as writer:
            for empresa in self.dict_bp.keys():
                self.dict_bp[empresa].to_excel(writer, sheet_name=empresa)

        # CREATE A EXCEL FILE - DFC
        with pd.ExcelWriter('..\\iq_capital\\fundamentos_limpo\\dfc.xlsx') as writer:
            for empresa in self.dict_dfc.keys():
                self.dict_dfc[empresa].to_excel(writer, sheet_name=empresa)

        # CREATE A EXCEL FILE - DRE
        with pd.ExcelWriter('..\\iq_capital\\fundamentos_limpo\\dre.xlsx') as writer:
            for empresa in self.dict_dre.keys():
                self.dict_dre[empresa].to_excel(writer, sheet_name=empresa)

    def indicadores(self):
        cols = ['roa', 'fco', 'lc', 'alavancagem', 'shares', 'ga']
        dict_dfs = {}

        for nome in self.nomes:
            print(nome)
            if nome == 'GOLL':
                print('paraa')
            # ROA = ATIVO TOTAL MEDIO/ LUCRO LIQUIDO
            ## ATIVO MEDIO
            ativo_total = self.dict_bp[nome].loc['Total Assets'].to_numpy().reshape(1, self.dict_bp[nome].loc['Total Assets'].count())
            ativo_total_1 = ativo_total[0][1:].reshape(1, len(ativo_total[0])-1)
            ativo_total_1[ativo_total_1 == 0] = 0.000000000000000000000000000000000000000001
            ativo_total_0 = ativo_total[0][:-1].reshape(1, len(ativo_total[0])-1)
            ativo_total_0[ativo_total_1 == 0] = 0.000000000000000000000000000000000000000001
            at_medio = np.divide(ativo_total_1, ativo_total_1 + ativo_total_0)

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

            # ALAVANCAGEM: PC/PC + PNC
            # po_curto = self.dict_bp[nome].loc['Curr. Port. of LT Debt'].to_numpy().reshape(1, self.dict_bp[nome].loc['Curr. Port. of LT Debt'].count())
            # po_longo = self.dict_bp[nome].loc['Long-Term Debt'].to_numpy().reshape(1, self.dict_bp[nome].loc['Long-Term Debt'].count())
            # passivo_o = po_curto + po_longo
            # ativo_total[ativo_total == 0] = 0.000000000000000000000000000000000000000001
            #
            # alavancagem = passivo_o/ativo_total

            ## PNC
            pnc = self.dict_bp[nome].loc['Total Current Liabilities'].to_numpy().reshape(1, self.dict_bp[nome].loc[
                'Total Current Liabilities'].count())
            pnc[pnc == 0] = 0.000000000000000000000000000000000000000001

            ## PASSIVO TOTAL
            passivo_t = self.dict_bp[nome].loc['Total Liabilities'].to_numpy().reshape(1, self.dict_bp[nome].loc[
                'Total Liabilities'].count())
            passivo_t[passivo_t == 0] = 0.000000000000000000000000000000000000000001
            alavancagem = pc / passivo_t

            # QTDE ACOES
            shares = self.dict_bp[nome].loc['Total Shares Out. on Balance Sheet Date'].to_numpy().reshape(1, self.dict_bp[nome].loc['Total Shares Out. on Balance Sheet Date'].count())

            # MARGEM BRUTA


            # GA = RECITA DE VENDAS LIQUIDA/ATIVO TOTAL MEDIO
            ## VENDAS LIQUIDAS
            vend_liq = self.dict_dre[nome].loc['Total Revenue'].to_numpy()[1:].reshape(1, self.dict_dre[nome].loc['Total Revenue'].count()-1)
            vend_liq[vend_liq == 0] = 0.000000000000000000000000000000000000000001

            ga = np.divide(vend_liq, at_medio)
            ga = np.insert(ga, 0, 0).reshape(1, self.dict_dre[nome].loc['Total Revenue'].count())

            # CREATE DF
            df = pd.DataFrame(np.concatenate((roa.T, fco.T, lc.T, alavancagem.T, shares.T, ga.T), axis=1), columns=cols)
            # ADD DICT
            dict_dfs[nome] = df

        # CREATE A EXCEL FILE
        with pd.ExcelWriter('..\\iq_capital\\fundamentos_limpo\\indicadores.xlsx') as writer:
            for empresa in dict_dfs.keys():
                dict_dfs[empresa].to_excel(writer, sheet_name=empresa)

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

        # CREATE A EXCEL FILE
        with pd.ExcelWriter('..\\iq_capital\\precos_limpo\\precos.xlsx') as writer:
            for empresa in self.dict_prices.keys():
                self.dict_prices[empresa].to_excel(writer, sheet_name=empresa, index=False)


def main():
    base_path = "..\\iq_capital\\fundamentos_sujos"
    price_path_folder = "..\\iq_capital\\precos_sujos"
    exp_b = exporta_base(base_path, price_path_folder=price_path_folder)

    # exp_b.limpa_base_f()

    exp_b.dict_bp = pd.read_excel('../iq_capital/fundamentos_limpo/bp.xlsx', index_col=0, sheet_name=None)
    exp_b.dict_dfc = pd.read_excel('../iq_capital/fundamentos_limpo/dfc.xlsx', index_col=0, sheet_name=None)
    exp_b.dict_dre = pd.read_excel('../iq_capital/fundamentos_limpo/dre.xlsx', index_col=0, sheet_name=None)
    exp_b.nomes = list(exp_b.dict_bp.keys())

    exp_b.indicadores() 

    # exp_b.dfs_prices()
    # exp_b.limpa_base_p()

if __name__ == '__main__':
    main()