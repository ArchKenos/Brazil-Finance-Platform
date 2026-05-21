import requests
from pathlib import Path
from datetime import datetime
import pandas as pd
import os
import json
import yfinance as yf

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

def ibovespa_components():

    df = pd.read_csv(r"C:\Users\bruno\Downloads/IBOVDia_20-05-26.csv",
                     encoding='latin1',
                     header=1,
                     sep=';',
                     index_col=False
                     )
    print(df.head())
    column_data = df.iloc[:, 0]
    ibovespa_tickets = []
    
    for ticket in column_data:
        formatted_ticket = f"{ticket}.SA"
        ibovespa_tickets.append(formatted_ticket)
    
    print(ibovespa_tickets)
if __name__ == "__main__":
    ibovespa_components()
    #data = extract_by_serie()
    #save_bronze_data(data)
