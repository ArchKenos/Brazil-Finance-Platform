import requests
from pathlib import Path
from datetime import datetime
import pandas as pd
import os
import json
import yfinance as yf
import base64

#URL de Extração

LAKE_DIR = Path("Bronze") / "raw"
prefix = "https://api.bcb.gov.br/dados/serie/bcdata.sgs."

today_time = datetime.today()
max_time = today_time.replace(year = today_time.year - 10)

max_time = str(max_time.strftime ("%d/%m/%Y"))
today_time = str(today_time.strftime ("%d/%m/%Y"))

def extract_by_serie(code: int = 11, InitialDate = max_time, FinalDate = today_time):
    url = f"{prefix}{code}/dados?formato=json&dataInicial={InitialDate}&dataFinal={FinalDate}#"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return() 

def save_bronze_data(data):
    
    LAKE_DIR.mkdir(parents=True, exist_ok=True)
    FILE_PATH = LAKE_DIR /"bronze_financedata.json"
    with open(FILE_PATH, 'w', encoding="UTF-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def return_ibovespa_info_json():
    base_url = "https://sistemaswebb3-listados.b3.com.br/indexProxy/indexCall/GetPortfolioDay/"
    parameters_url = {"language":"pt-br",
                      "pageNumber":"1",
                      "pageSize":"120",
                      "index":"IBOV",
                      "segment":"1"
                      }
    parameters_json = json.dumps(parameters_url)
    
    parameterb64 = base64.urlsafe_b64encode(parameters_json.encode('utf-8')).decode('utf-8')

    api_url = f'{base_url}{parameterb64}'
    response = requests.get(api_url)
    response.raise_for_status()
    response = response.json()
    
    return response

def return_ibovespa_stocks():

    response = return_ibovespa_info_json()
    df = pd.DataFrame(response["results"])
    stocks = df["cod"].dropna().tolist()
    
    
    formatted_stocks = [f"{cod}.SA" for cod in stocks] 
        
    print(formatted_stocks)
if __name__ == "__main__":
    return_ibovespa_stocks()
    #data = extract_by_serie()
    #save_bronze_data(data)
