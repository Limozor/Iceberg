import os
import time
import requests

from info import VirusTotal_API

class VirusTotalScanner:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.virustotal.com/api/v3"

        self.headers = {
            "x-apikey": self.api_key
        }

    def upload_file(self, file_path):
        """
        Загружает файл на VirusTotal
        и возвращает ID анализа.
        """

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл не найден: {file_path}")

        file_size = os.path.getsize(file_path)

        max_size = 32 * 1024 * 1024

        if file_size > max_size:
            raise ValueError(
                "Файл слишком большой. "
                "Максимальный размер для бесплатного API — 32 МБ."
            )

        with open(file_path, "rb") as file:

            files = {
                "file": (
                    os.path.basename(file_path),
                    file
                )
            }

            response = requests.post(
                f"{self.base_url}/files",
                headers=self.headers,
                files=files
            )

        if response.status_code == 429:
            raise Exception(
                "Превышен лимит запросов VirusTotal API."
            )

        if response.status_code != 200:
            raise Exception(
                f"Ошибка загрузки файла: "
                f"{response.status_code}\n{response.text}"
            )

        data = response.json()

        return data["data"]["id"]

    def get_analysis_report(self, analysis_id):
        """
        Получает отчёт анализа.
        """

        url = f"{self.base_url}/analyses/{analysis_id}"

        for _ in range(10):

            response = requests.get(
                url,
                headers=self.headers
            )

            if response.status_code == 429:
                time.sleep(60)
                continue

            if response.status_code != 200:
                time.sleep(10)
                continue

            report = response.json()

            status = report["data"]["attributes"]["status"]

            if status == "completed":

                stats = report["data"]["attributes"]["stats"]

                sha256 = (
                    report.get("meta", {})
                    .get("file_info", {})
                    .get("sha256")
                )

                return {
                    "malicious": stats.get("malicious", 0),
                    "suspicious": stats.get("suspicious", 0),
                    "harmless": stats.get("harmless", 0),
                    "undetected": stats.get("undetected", 0),
                    "total": sum(stats.values()),
                    "sha256": sha256,
                    "report_url": (
                        f"https://www.virustotal.com/gui/file/{sha256}"
                        if sha256 else None
                    )
                }

            elif status in ["queued", "in_progress"]:
                time.sleep(15)

            else:
                raise Exception(
                    f"Неожиданный статус анализа: {status}"
                )

        raise Exception(
            "Анализ не завершился вовремя."
        )

    def scan_photo(self, photo_path):
        """
        Полное сканирование фотографии.
        """

        analysis_id = self.upload_file(photo_path)

        return self.get_analysis_report(
            analysis_id
        )


def VT_report(photo_path):
    scanner = VirusTotalScanner(VirusTotal_API)
    result = scanner.scan_photo(photo_path)
    return result
