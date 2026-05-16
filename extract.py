import requests
from pathlib import Path
from datetime import datetime

#URL de Extração

LAKE_DIR = Path("Bronze") / "raw"
prefix = "https://api.bcb.gov.br/dados/serie/bcdata.sgs."

today_time = datetime.today()
max_time = today_time.replace(year = today_time.year - 10)

max_time = str(max_time.strftime ("%d/%m/%Y"))
today_time = str(today_time.strftime ("%d/%m/%Y"))

def extract_by_serie(codigo_serie, dataInicial = max_time, dataFinal = today_time):
    url = f"{prefix}{codigo_serie}/dados?formato=json&dataInicial={dataInicial}&dataFinal={dataFinal}#"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json
    except requests.exceptions.RequestException as e:
        return() 
    
