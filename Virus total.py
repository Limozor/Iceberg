# API Virus Total 078f4d675bdb34ee990436e84009d17a0a9997229a9b23f403533cdaa0055b97

import os
import time
import requests

class VirusTotalScanner:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.virustotal.com/api/v3"
        self.headers = {
            "x-apikey": self.api_key,
            "Accept": "application/json"
        }

    def upload_file(self, file_path):
        """Загружает файл на VirusTotal и возвращает ID анализа."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл не найден: {file_path}")

        # Бесплатный лимит VirusTotal — 32 МБ (для платных 650 МБ)
        file_size = os.path.getsize(file_path)
        if file_size > 32 * 1024 * 1024:  # 32 МБ
            raise ValueError("Файл слишком большой. Максимальный размер для бесплатного API — 32 МБ.")

        # Получаем URL для загрузки
        response = requests.get(
            f"{self.base_url}/files/upload_url",
            headers=self.headers
        )
        if response.status_code != 200:
            raise Exception(f"Ошибка получения URL загрузки: {response.status_code}")

        upload_url = response.json()['data']

        # Загружаем файл
        with open(file_path, 'rb') as file:
            files = {'file': (os.path.basename(file_path), file)}
            response = requests.post(upload_url, files=files, headers=self.headers)

        if response.status_code == 200:
            analysis_id = response.json()['data']['id']
            print(f"Файл загружен. ID анализа: {analysis_id}")
            return analysis_id
        else:
            raise Exception(f"Ошибка загрузки файла: {response.status_code} - {response.text}")

    def get_analysis_report(self, analysis_id):
        """Получает отчёт о сканировании по ID."""
        url = f"{self.base_url}/analyses/{analysis_id}"

        for attempt in range(3):
            response = requests.get(url, headers=self.headers)

            if response.status_code == 200:
                report = response.json()
                status = report['data']['attributes']['status']

                if status == 'completed':
                    stats = report['data']['attributes']['stats']
                    print("\n=== ОТЧЁТ О СКАНИРОВАНИИ ===")
                    print(f"Всего антивирусов: {sum(stats.values())}")
                    print(f"Обнаружено угроз: {stats.get('malicious', 0)}")
                    print(f"Подозрительно: {stats.get('suspicious', 0)}")
                    print(f"Безопасно: {stats.get('harmless', 0)}")
                    print(f"Не определено: {stats.get('undetected', 0)}")

                    file_id = report['meta']['file_info']['sha256']
                    print(f"\nПолный отчёт: https://www.virustotal.com/gui/file/{file_id}")

                    return report

                elif status == 'queued' or status == 'in_progress':
                    print(f"Анализ ещё выполняется... Попытка {attempt + 1}/3")
                    time.sleep(10)

                else:
                    raise Exception(f"Неожиданный статус анализа: {status}")
            else:
                print(f"Ошибка запроса отчёта: {response.status_code}")
                time.sleep(5)

        # Если после 3 попыток не завершился
        raise Exception("Анализ не завершился в течение заданного времени.")

    def scan_photo(self, photo_path):
        """Основная функция для сканирования фотографии."""
        try:
            print(f"Начинаем сканирование фото: {photo_path}")
            analysis_id = self.upload_file(photo_path)
            report = self.get_analysis_report(analysis_id)
            return report
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            return None


if __name__ == "__main__":
    # ВАЖНО: замените на ваш API-ключ с virustotal.com
    API_KEY = "ваш_api_ключ_здесь"
    PHOTO_PATH = "photo.jpg"  # замените на путь к вашей фотографии

    scanner = VirusTotalScanner(API_KEY)
    result = scanner.scan_photo(PHOTO_PATH)