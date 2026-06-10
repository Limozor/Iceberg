import requests
from info import Google_link_API


API_KEY = Google_link_API
API_URL = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={API_KEY}"


def check_url_safety(url_to_check):
    payload = {
        "client": {"clientId": "my_python_app", "clientVersion": "1.0.0"},
        "threatInfo": {
            "threatTypes": [
                "MALWARE",
                "SOCIAL_ENGINEERING",
                "UNWANTED_SOFTWARE",
                "POTENTIALLY_HARMFUL_APPLICATION",
            ],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url_to_check}],
        },
    }

    try:
        response = requests.post(API_URL, json=payload, timeout=10)
        response.raise_for_status()

        if not response.text.strip() or response.json() == {}:
            return {"status": "Безопасно", "message": f"Проверяемая ссылка: {url_to_check}"}

        data = response.json()
        if "matches" in data:
            threats = [match["threatType"] for match in data["matches"]]
            return {
                "status": "Опасно",
                "message": f"Ссылка {url_to_check} ОПАСНА!",
                "threats": threats,
            }

        return {"status": "unknown", "message": "Неизвестный формат ответа от API."}

    except requests.exceptions.HTTPError as http_err:
        return {"status": "error", "message": f"Ошибка HTTP: {http_err}. Проверьте API-ключ."}
    except Exception as err:
        return {"status": "error", "message": f"Ошибка соединения: {err}"}