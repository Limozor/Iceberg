import time
import requests
from info import VirusTotal_API


class VirusTotalScanner:
    def __init__(self, api_key):
        self.base_url = "https://www.virustotal.com/api/v3"
        self.headers = {"x-apikey": api_key}

    def upload_file(self, file_path):
        with open(file_path, "rb") as file:
            response = requests.post(
                f"{self.base_url}/files",
                files={"file": file},
                headers=self.headers
            )

        if response.status_code != 200:
            raise Exception(f"Ошибка загрузки: {response.status_code}\n{response.text}")

        return response.json()["data"]["id"]

    def get_analysis_report(self, analysis_id):
        url = f"{self.base_url}/analyses/{analysis_id}"

        for _ in range(10):
            response = requests.get(url, headers=self.headers)
            if response.status_code != 200:
                time.sleep(10)
                continue

            report_data = response.json().get("data", {})
            attributes = report_data.get("attributes", {})
            status = attributes.get("status")

            if status == "completed":
                stats = attributes.get("stats", {})

                malicious = stats.get("malicious", 0)
                suspicious = stats.get("suspicious", 0)

                # [Ошибка, Вирусы, Подозрительный]
                is_malicious = malicious > 0
                is_suspicious = suspicious > 0
                report = [False, is_malicious, is_suspicious]

                if is_malicious or is_suspicious:
                    report.append(
                        f"VirusTotal обнаружил угрозы! Вредоносных движков: {malicious}, Подозрительных: {suspicious}."
                    )

                return report

            elif status in ["queued", "in_progress"]:
                time.sleep(15)
            elif status == "failed":
                raise Exception("Анализ завершился с ошибкой.")
            else:
                raise Exception(f"Неожиданный статус: {status}")

        raise Exception("Превышено время ожидания анализа.")

    def scan_file(self, file_path):
        try:
            analysis_id = self.upload_file(file_path)
            return self.get_analysis_report(analysis_id)
        except Exception as e:
            return [True, False, False, f"Ошибка при работе с VirusTotal: {str(e)}"]


def Virus_Total_Scan(file_path):
    scanner = VirusTotalScanner(VirusTotal_API)
    return scanner.scan_file(file_path)