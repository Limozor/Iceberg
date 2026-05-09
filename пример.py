import requests
from pathlib import Path

VIRUSTOTAL_API_KEY = "ваш_ключ"  # получите на virustotal.com

def scan_with_virustotal(file_path: str):
    url = "https://www.virustotal.com/api/v3/files"
    headers = {"x-apikey": VIRUSTOTAL_API_KEY}
    with open(file_path, "rb") as f:
        files = {"file": (Path(file_path).name, f)}
        response = requests.post(url, headers=headers, files=files)
    if response.status_code == 200:
        data = response.json()
        analysis_id = data['data']['id']
        # Потом нужно запросить результат по analysis_id...
        return analysis_id
    else:
        return None