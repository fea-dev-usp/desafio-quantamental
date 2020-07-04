import funcoes
import json
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials


# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('gspread\client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("bot_perform_sheet").sheet1

btc_value = funcoes.get_btc_value()
sheet.update_cell(2,1,btc_value)

dolar_value = funcoes.get_dolar_value()
sheet.update_cell(2,2,dolar_value)


client_id = 'hbhLfeWi5VXQAYLqscg-58_w'
client_secret = 'TUXX2-OD7X_JvP2TTJn8g0uYWIrKmDWEnUlDMOuiZs_FWqJK'

# sou de mais