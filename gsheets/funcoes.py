import funcoes
import json
import requests
import gspread
import urllib
from oauth2client.service_account import ServiceAccountCredentials

def get_btc_value():
    request_btc = requests.get('https://www.mercadobitcoin.net/api/BTC/ticker/')
    btc_ticker = json.loads(request_btc.content.decode('UTF-8'))
    btc_buy = float(btc_ticker['ticker']['buy'])
    return btc_buy

def get_dolar_value(): 
    request_dolar = requests.get('https://economia.awesomeapi.com.br/all/USD-BRL')
    dolar_ticker = json.loads(request_dolar.content.decode('UTF-8'))
    dolar_sell = float(dolar_ticker["USD"]['ask'].replace(",","."))

    return dolar_sell

