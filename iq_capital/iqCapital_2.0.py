from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import pandas as pd
from selenium.webdriver.chrome.options import Options
from time import sleep
from os import listdir, remove
from os.path import isfile, join

# options = Options()
#
# # options.add_argument("--headless")      # Runs Chrome in headless mode.
# # options.add_argument('--no-sandbox')    # Bypass OS security model
# # options.add_argument('--disable-gpu')   # applicable to windows os only
# # options.add_argument('start-maximized')
# # options.add_argument('disable-infobars')
# # options.add_argument("--disable-extensions")

# driver = webdriver.Chrome("C:\\Nícolas\\FEA.dev\\iq_capital\\chromedriver.exe", options=options)
# initial_url = "https://www.capitaliq.com/ciqdotnet/login-sso.aspx?bmctx=202C7940E5B3C784A1D977EF9E24AB0D&contextType=external&username=string&enablePersistentLogin=true&OverrideRetryLimit=0&contextValue=%2Foam&password=secure_string&challenge_url=https%3A%2F%2Fwww.capitaliq.com%2Fciqdotnet%2Flogin-sso.aspx&request_id=5780355017588001025&authn_try_count=0&locale=pt_BR&resource_url=https%253A%252F%252Fwww.capitaliq.com%252Fciqdotnet%252Flogin.aspx"
# driver.get(initial_url)
# print(driver.title)
#
# # sleep(5)
# # driver.find_element_by_xpath()
#
# driver.close()

class iq_capital_fundamentos():
    def __init__(self, username, password, driver, download_path):
        self.password = password
        self.username = username
        self.driver = driver
        self.d_path = download_path

    def try_click(self, driver, path, count=3):
        for i in range(count):
            try:
                element = driver.find_element_by_xpath(path)
                element.click()
                return element
            except:
                sleep(0.5)

    def try_send_keys(self, driver, path, keys, count=3):
        for i in range(count):
            try:
                element = driver.find_element_by_xpath(path)
                element.send_keys(keys)
                break
            except:
                sleep(0.5)

    def login(self):
        # PAG INICIAL
        initial_url = "https://www.capitaliq.com"
        self.driver.get(initial_url)

        self.driver.find_element_by_xpath(
            "/html/body/div[1]/div[3]/div[1]/form/table/tbody/tr[1]/td/ol/li[1]/input"
        ).send_keys(self.username)

        self.driver.find_element_by_xpath(
            "/html/body/div[1]/div[3]/div[1]/form/table/tbody/tr[1]/td/ol/li[2]/input"
        ).send_keys(self.password)

        self.driver.find_element_by_xpath(
            "/html/body/div[1]/div[3]/div[1]/form/table/tbody/tr[1]/td/ol/li[5]/input"
        ).click()

    def acha_empresa(self, nome):
        self.try_send_keys(self.driver,
                           "/html/body/div[2]/table/tbody/tr/td[2]/div/form[2]/table/tbody/tr/td[1]/div[1]/div/input",
                           nome)
        self.try_click(self.driver, "/html/body/div[2]/table/tbody/tr/td[2]/div/form[2]/table/tbody/tr/td[2]/input")

    def dre(self):
        self.try_click(self.driver, "/html/body/table/tbody/tr[2]/td[2]/span[1]/div/span[13]/div[3]/a")
        # TRIMESTRAL
        self.try_click(self.driver,
                       "/html/body/table/tbody/tr[2]/td[4]/div/form/table/tbody/tr[1]/td/div[1]/div[4]/table/tbody/tr[2]/td[2]/select/option[2]")
        # STANDARD
        drop_down = Select(self.driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[4]/div/form/table/tbody/tr[1]/td/div[1]/div[4]/table/tbody/tr[1]/td[2]/select'))
        # select by visible text
        drop_down.select_by_visible_text('Standard')
        # GO
        self.try_click(self.driver,
                       "/html/body/table/tbody/tr[2]/td[4]/div/form/table/tbody/tr[1]/td/div[1]/div[4]/table/tbody/tr[2]/td[6]")
        # TODOS OS ANOS DISPONIVEIS
        self.try_click(self.driver,
                       "/html/body/table/tbody/tr[2]/td[4]/div/form/table/tbody/tr[1]/td/div[3]/table/tbody/tr/td/div[1]/div/div[2]/div/a")
        # ADD TO DOWNLOAD
        self.try_click(self.driver,
                       "/html/body/table/tbody/tr[2]/td[4]/div/form/table/tbody/tr[1]/td/div[1]/div[2]/div[2]/ul/li[8]/div/map/area[2]")
        self.try_click(self.driver,
                       "/html/body/table/tbody/tr[2]/td[4]/div/form/table/tbody/tr[1]/td/div[1]/div[2]/div[4]/div/a[2]/span")
        sleep(1)

    def balanco(self):
        self.try_click(self.driver, "/html/body/table/tbody/tr[2]/td[2]/span[1]/div/span[13]/div[4]/a")
        # TRIMESTRAL
        self.try_click(self.driver,
                       "/html/body/table/tbody/tr[2]/td[4]/div/form/table/tbody/tr[1]/td/div[1]/div[4]/table/tbody/tr[2]/td[2]/select/option[2]")
        # STANDARD
        drop_down = Select(self.driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[4]/div/form/table/tbody/tr[1]/td/div[1]/div[4]/table/tbody/tr[1]/td[2]/select'))
        # select by visible text
        drop_down.select_by_visible_text('Standard')
        # GO
        self.try_click(self.driver,
                       "/html/body/table/tbody/tr[2]/td[4]/div/form/table/tbody/tr[1]/td/div[1]/div[4]/table/tbody/tr[2]/td[6]")
        # TODOS OS ANOS DISPONIVEIS
        self.try_click(self.driver,
                       "/html/body/table/tbody/tr[2]/td[4]/div/form/table/tbody/tr[1]/td/div[3]/table/tbody/tr/td/div[1]/div/div[2]/div/a")

        # ADD TO DOWNLOAD
        self.try_click(self.driver,
                       "/html/body/table/tbody/tr[2]/td[4]/div/form/table/tbody/tr[1]/td/div[1]/div[2]/div[2]/ul/li[8]/div/map/area[2]")
        self.try_click(self.driver,
                       "/html/body/table/tbody/tr[2]/td[4]/div/form/table/tbody/tr[1]/td/div[1]/div[2]/div[4]/div/a[2]/span")
        sleep(1)

    def dfc(self):
        self.try_click(self.driver, "/html/body/table/tbody/tr[2]/td[2]/span[1]/div/span[13]/div[5]/a")
        # TRIMESTRAL
        self.try_click(self.driver,
                       "/html/body/table/tbody/tr[2]/td[4]/div/form/table/tbody/tr[1]/td/div[1]/div[4]/table/tbody/tr[2]/td[2]/select/option[2]")
        # STANDARD
        drop_down = Select(self.driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[4]/div/form/table/tbody/tr[1]/td/div[1]/div[4]/table/tbody/tr[1]/td[2]/select'))
        # select by visible text
        drop_down.select_by_visible_text('Standard')
        # GO
        self.try_click(self.driver,
                       "/html/body/table/tbody/tr[2]/td[4]/div/form/table/tbody/tr[1]/td/div[1]/div[4]/table/tbody/tr[2]/td[6]")
        # TODOS OS ANOS DISPONIVEIS
        self.try_click(self.driver,
                       "/html/body/table/tbody/tr[2]/td[4]/div/form/table/tbody/tr[1]/td/div[3]/table/tbody/tr/td/div[1]/div/div[2]/div/a")

        # ADD TO DOWNLOAD
        self.try_click(self.driver,
                       "/html/body/table/tbody/tr[2]/td[4]/div/form/table/tbody/tr[1]/td/div[1]/div[2]/div[2]/ul/li[8]/div/map/area[2]")
        self.try_click(self.driver,
                       "/html/body/table/tbody/tr[2]/td[4]/div/form/table/tbody/tr[1]/td/div[1]/div[2]/div[4]/div/a[2]/span")
        sleep(1)

    def download(self):
        sleep(1)
        self.try_click(self.driver,
                       "/html/body/table/tbody/tr[2]/td[4]/div/form/table/tbody/tr[1]/td/div[1]/div[2]/div[2]/ul/li[9]/a/div")
        self.try_click(self.driver,
                       "/html/body/table/tbody/tr[2]/td[4]/div/form/table/tbody/tr[1]/td/div[1]/div[2]/div[5]/div[2]/div/div[4]/div[5]/a[3]/img")

    def check_download(self, tipo='fundamentos', count=0):
        sleep(4)
        onlyfiles = [f for f in listdir(self.d_path) if isfile(join(self.d_path, f))]

        # FUNDAMENTOS
        if tipo == 'fundamentos':
            if True in [True for x in onlyfiles if "Default Binder" in x]:
                pass
            else:
                self.download()
                self.check_download()

        # PRICES
        elif tipo == 'precos':
            if count == len([True for x in onlyfiles if "Charting Excel Export" in x]):
                pass
            else:
                self.check_download(tipo='precos', count=count)

        # INDEX
        elif tipo == 'index':
            if count == len([True for x in onlyfiles if "Charting Excel Export" in x]):
                pass
            else:
                self.check_download(tipo='index', count=count)

    def exclui_download(self):
        onlyfiles = [f for f in listdir(self.d_path) if isfile(join(self.d_path, f))]
        # if True in [True for x in onlyfiles if "Default Binder" in x]:
        #     for file in [x for x in onlyfiles if "Default Binder" in x]:
        #         remove(self.d_path + "\\" + file)
        for file in onlyfiles:
            remove(self.d_path + "\\" + file)

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

    def delet_list(self):

        self.try_click(self.driver,
                       "/html/body/table/tbody/tr[2]/td[4]/div/form/table/tbody/tr[1]/td/div[1]/div[2]/div[2]/ul/li[9]/a/div")
        self.try_click(self.driver,
                       "/html/body/table/tbody/tr[2]/td[4]/div/form/table/tbody/tr[1]/td/div[1]/div[2]/div[5]/div[2]/div/div[4]/div[3]/span[3]/a")
        self.driver.switch_to.alert.accept()
        sleep(10)

    def index_already_exixt(self, tickers, base, path_base_folder):
        """

        :param tickers:
        :param base: can be: 'Demons', 'Price'
        :return: a list
        """

        # CHECK IN DEMOSNTRATIVOS (FUNDAMENTOS)
        if 'Demons' == base:
            # ARRUMA TICKERS
            t = set([x[:4] for x in tickers])

            # LE AS BASES DE DADOS
            dre = pd.HDFStore(path_base_folder + '\\dre.h5')
            dfc = pd.HDFStore(path_base_folder + '\\dfc.h5')
            bp = pd.HDFStore(path_base_folder + '\\bp.h5')

            # SET COM AS EMPRESAS QUE N ESTAO NA BASE
            dif_names = set([x for x in t if x not in dre])
            dif_names.update(t.difference(set([x for x in t if x not in dfc])))
            dif_names.update(t.difference(set([x for x in t if x not in bp])))

            # CLOSE
            dre.close()
            dfc.close()
            bp.close()

            return list(dif_names)

        # CHECK IN PRECOS
        elif 'Prices' == base:
            # ARRUMA TICKERS
            t = set(tickers)

            # LE AS BASES DE DADOS
            prices = pd.HDFStore(path_base_folder + '\\precos.h5')

            # SET COM AS EMPRESAS QUE N ESTAO NA BASE
            dif_names = set([x for x in t if x not in prices])

            # CLOSE HDF5
            prices.close()

            return list(dif_names)

        # CHECK IN INDEX
        elif 'Index' == base:
            # ARRUMA TICKERS
            t = set(tickers)

            # LE AS BASES DE DADOS
            index = pd.HDFStore(path_base_folder + '\\index.h5')

            # SET COM AS EMPRESAS QUE N ESTAO NA BASE
            dif_names = set([x for x in t if x not in index])

            # CLOSE
            index.close()

            return list(dif_names)

    def get_fund(self, tickers, demonstrativos, path_base_limpa='..\\iq_capital\\fundamentos_limpo'):
        # EXCLUI BASES SUJAS
        self.exclui_download()

        # VERIFICA SE AS EMPRESAS JA ESTPA NA BASE
        dif_tickers = self.index_already_exixt(tickers, 'Demons', path_base_limpa)

        # LOGIN
        self.login()

        # Initial call to print 0% progress
        l = len(tickers)
        self.printProgressBar(0, l, prefix='Progress:', suffix='Complete', length=50)
        for i in range(len(dif_tickers)):
            # VERFICA SE ATINGIIU O MAXIMO DE ABAS EM UM UNICO EXCEL
            if i/198 == 0 and i != 0:
                # DOWNLOAD
                self.download()
                self.check_download()
                self.delet_list()

            # PROCURA A EMPRESA
            self.acha_empresa("BOVESPA:{}".format(dif_tickers[i]))

            # DRE
            if "DRE" in demonstrativos:
                self.dre()

            # BALANCO
            if "B" in demonstrativos:
                self.balanco()

            # DFC
            if "DFC" in demonstrativos:
                self.dfc()

            # Update Progress Bar
            self.printProgressBar(i + 1, l, prefix='Progress:', suffix='Complete', length=50)

        # DOWNLOAD
        self.download()
        self.check_download()
        self.delet_list()

        # CLOSE DRIVER
        self.driver.__exit__()

    def shares_price(self, tickers, ano_ini=None, ano_fim=None):
        # EXCLUI BASES SUJAS
        self.exclui_download()

        # VERIFICA SE AS EMPRESAS JA ESTPA NA BASE
        dif_tickers = self.index_already_exixt(tickers, 'Prices', '..\\iq_capital\\precos_limpo')

        # LOGIN
        self.login()

        # PROCURA A EMPRESA
        self.acha_empresa("BOVESPA:{}".format(tickers[0]))

        # ABA DOS PRECOS
        self.try_click(self.driver, "/html/body/table/tbody/tr[2]/td[2]/span[1]/div/span[24]/div[2]/a")
        sleep(7)

        # PERIODO MAX
        self.try_click(self.driver,
                       "/html/body/table/tbody/tr[2]/td[4]/div/form/div[3]/div/div/div[1]/div[2]/div/div[6]/div[1]/button[9]")
        sleep(7)

        # AJUSTA COM BASE NO DIVIDENDO
        self.try_click(self.driver,
                       "/html/body/table/tbody/tr[2]/td[4]/div/form/div[3]/div/div/div[1]/div[2]/div/div[4]/div/button")
        sleep(3)
        self.try_click(self.driver,
                       "/html/body/table/tbody/tr[2]/td[4]/div/form/div[3]/div/div/div[1]/div[2]/div/div[4]/div[2]/div/div[2]/div/ul/li[1]/label")
        self.try_click(self.driver,
                       "/html/body/table/tbody/tr[2]/td[4]/div/form/div[3]/div/div/div[1]/div[2]/div/div[4]/div[2]/div/div[2]/div/ul/li[3]/label")
        sleep(9)

        count = 0
        for t in dif_tickers:
            count += 1
            # PESQUISA EMPRESA
            self.try_click(self.driver,
                           "/html/body/table/tbody/tr[2]/td[4]/div/form/div[3]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]")
            self.try_send_keys(self.driver,
                               "/html/body/table/tbody/tr[2]/td[4]/div/form/div[3]/div/div/div[1]/div[2]/div/div[1]/div/div/div/div/div[1]/input",
                               "BOVESPA:{}".format(t))
            self.try_send_keys(self.driver,
                               "/html/body/table/tbody/tr[2]/td[4]/div/form/div[3]/div/div/div[1]/div[2]/div/div[1]/div/div/div/div/div[1]/input",
                               Keys.ENTER)
            sleep(8)
            # DOWNLOAD
            self.try_click(self.driver,
                           "/html/body/table/tbody/tr[2]/td[4]/div/form/div[3]/div/div/div[1]/div[1]/div/div[2]/button[3]")
            self.check_download(tipo='precos', count=count)

        # CLOSE DRIVER
        self.driver.__exit__()

    def index_value(self, index=['IBOV']):
        # EXCLUI BASES SUJAS
        self.exclui_download()

        # VERIFICA SE AS EMPRESAS JA ESTPA NA BASE
        dif_index = self.index_already_exixt(index, 'Index', '..\\iq_capital\\index_limpo')

        # LOGIN
        self.login()

        # PROCURA A INDEX
        self.acha_empresa(dif_index[0])

        # ABA DOS VALORES
        self.try_click(self.driver, "/html/body/table/tbody/tr[2]/td[2]/span[1]/div/span[24]/div[2]/a")
        sleep(7)

        # PERIODO MAX
        self.try_click(self.driver,
                       "/html/body/table/tbody/tr[2]/td[4]/div/form/div[3]/div/div/div[1]/div[2]/div/div[6]/div[1]/button[9]")
        sleep(7)

        # PROCURA INDEX
        count = 0
        for i in dif_index:
            count += 1
            # PESQUISA INDEX
            self.try_click(self.driver,
                           "/html/body/table/tbody/tr[2]/td[4]/div/form/div[3]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]")
            self.try_send_keys(self.driver,
                               "/html/body/table/tbody/tr[2]/td[4]/div/form/div[3]/div/div/div[1]/div[2]/div/div[1]/div/div/div/div/div[1]/input",
                               i)
            self.try_send_keys(self.driver,
                               "/html/body/table/tbody/tr[2]/td[4]/div/form/div[3]/div/div/div[1]/div[2]/div/div[1]/div/div/div/div/div[1]/input",
                               Keys.ENTER)
            sleep(8)
            # DOWNLOAD
            self.try_click(self.driver,
                           "/html/body/table/tbody/tr[2]/td[4]/div/form/div[3]/div/div/div[1]/div[1]/div/div[2]/button[3]")
            self.check_download(tipo='index', count=count)

        # CLOSE DRIVER
        self.driver.__exit__()


def fundamentos():

    # LOGIN / SENHA
    username = "nicolas.zanonidh@usp.br"
    password = "apto213A"
    # tickers = [
    #     'ABEV3', 'AZUL4', 'B3SA3', 'BBAS3', 'BBDC3', 'BBDC4', 'BBSE3', 'BEEF3', 'BPAC11', 'BRAP4', 'BRDT3', 'BRFS3',
    #     'BRKM5', 'BRML3', 'BTOW3', 'CCRO3', 'CIEL3', 'CMIG4', 'COGN3', 'CPFE3', 'CRFB3', 'CSAN3', 'CSNA3', 'CVCB3',
    #     'CYRE3', 'ECOR3', 'EGIE3', 'ELET3', 'ELET6', 'EMBR3', 'ENBR3', 'ENGI11', 'EQTL3', 'FLRY3', 'GGBR4', 'GNDI3',
    #     'GOAU4', 'GOLL4', 'HAPV3', 'HGTX3', 'HYPE3', 'IGTA3', 'IRBR3', 'ITSA4', 'ITUB4', 'JBSS3', 'KLBN11', 'LAME4',
    #     'LREN3', 'MGLU3', 'MRFG3', 'MRVE3', 'MULT3', 'NTCO3', 'PCAR3', 'PETR3', 'PETR4', 'QUAL3', 'RADL3', 'RAIL3',
    #     'RENT3', 'SANB11', 'SBSP3', 'SULA11', 'SUZB3', 'TAEE11'
    # ]

    tickers = ['OIBR4', 'ABEV3', 'AZUL4', 'B3SA3', 'BBAS3']

    demons = ['DRE', 'B', 'DFC']

    # DOWNLOAD FUNDAMENTOS
    # INICIA O WEBDRIVER
    download_path_fundamentos = "C:\\Nícolas\\FEA.dev\\desafio-quantamental\\iq_capital\\fundamentos_sujos"
    f_options = webdriver.ChromeOptions()
    # options.gpu = False
    # options.headless = True
    f_options.add_experimental_option("prefs", {
        "download.default_directory": download_path_fundamentos,
        'profile.default_content_setting_values.automatic_downloads': 2,
    })

    desired = f_options.to_capabilities()
    desired['loggingPrefs'] = {'performance': 'ALL'}
    driver = webdriver.Chrome("..\\iq_capital\\chromedriver.exe", desired_capabilities=desired)

    iq_f = iq_capital_fundamentos(username, password, driver, download_path_fundamentos)
    # DEMONSTRATIVOS
    iq_f.get_fund(tickers, demons)

def shares():
    # LOGIN / SENHA
    username = "nicolas.zanonidh@usp.br"
    password = "apto213A"
    # TICKERS
    tickers = ['OIBR4', 'ABEV3', 'AZUL4', 'B3SA3', 'BBAS3']

    # INICIA O WEBDRIVER
    download_path_precos = "C:\\Nícolas\\FEA.dev\\desafio-quantamental\\iq_capital\\precos_sujos"
    f_options = webdriver.ChromeOptions()
    # options.gpu = False
    # options.headless = True
    f_options.add_experimental_option("prefs", {
        "download.default_directory": download_path_precos,
        'profile.default_content_setting_values.automatic_downloads': 1,
    })

    desired = f_options.to_capabilities()
    desired['loggingPrefs'] = {'performance': 'ALL'}
    driver_p = webdriver.Chrome("..\\iq_capital\\chromedriver.exe", desired_capabilities=desired)
    iq_p = iq_capital_fundamentos(username, password, driver_p, download_path_precos)
    # PRECOS ACOES
    iq_p.shares_price(tickers)

def index():
    # LOGIN / SENHA
    username = "nicolas.zanonidh@usp.br"
    password = "apto213A"
    # TICKERS
    index = ['IBOV']

    # INICIA O WEBDRIVER
    download_path_precos = "C:\\Nícolas\\FEA.dev\\desafio-quantamental\\iq_capital\\index_sujos"
    f_options = webdriver.ChromeOptions()
    # options.gpu = False
    # options.headless = True
    f_options.add_experimental_option("prefs", {
        "download.default_directory": download_path_precos,
        'profile.default_content_setting_values.automatic_downloads': 1,
    })

    desired = f_options.to_capabilities()
    desired['loggingPrefs'] = {'performance': 'ALL'}
    driver_p = webdriver.Chrome("..\\iq_capital\\chromedriver.exe", desired_capabilities=desired)
    iq_i = iq_capital_fundamentos(username, password, driver_p, download_path_precos)
    # VALOR INDEX
    iq_i.index_value(index)

if __name__ == '__main__':
    # fundamentos()
    # shares()
    index()

