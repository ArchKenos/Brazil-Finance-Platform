import requests
from pathlib import Path
from datetime import datetime
import os
import json

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


if __name__ == "__main__":
    data = extract_by_serie()
    save_bronze_data(data)
