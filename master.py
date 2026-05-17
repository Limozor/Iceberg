from pathlib import Path
import random

from VirusTotal import VT_report


# Проверка на скрытые данные в конце файла (EOF)
def check_image_EOF(master_file):
    signatures = [b'\xff\xd9', b'\x00\x00\x49\x45\x4e\x44\xae\x42\x60\x82']
    with open(master_file, 'rb') as f:
        content = f.read()
        for sig in signatures:
            if content.endswith(sig):
                return "Скрытые данные в конце фото не найдены"
    return "Внимание: в файле обнаружен вредоносный код (подозрительный конец файла)"


def is_suspicious(master_file):
    safe_suffixes = {'.png', '.jpg', '.jpeg'}
    path = Path(master_file)
    suffixes = path.suffixes
    if len(suffixes) >= 2:
        return "Количество расширений не допустимо (двойные расширения)"
    last_suffix = path.suffix.lower()
    if last_suffix not in safe_suffixes:
        return "Расширение не безопасно"
    return "Расширение безопасно"


def main_function(file_path):
    # Включение функций проверки и передача названия файла
    ci_OEF = check_image_EOF(file_path)
    susp = is_suspicious(file_path)
    vt_result = VT_report(file_path)

    # Сохранение полного отчета в файл
    report_dir = Path("reports")
    report_dir.mkdir(parents=True, exist_ok=True)
    base_name = Path(file_path).stem
    random_num = random.randint(100, 999)
    report_filename = f"{base_name}_report_{random_num}.txt"
    report_path = report_dir / report_filename

    report_file_data = f""""Отчет
    OEF проверка: {ci_OEF}
    
    Проверака расширений: {susp}
    
    VirusTotal:
    Обнаружено вирусов: {vt_result['malicious']}
    Подозрительно: {vt_result['suspicious']}
    Безвредные: {vt_result['harmless']}
    Безопастные: {vt_result['undetected']}
    Проверено: {vt_result['total']}
    SHA256: {vt_result['sha256']}
    Ссылка на проверку: {vt_result['report_url']}"""

    report_path.write_text(report_file_data, encoding="utf-8")

    # Возврат отчета
    return {
        f"""Краткий отчет о выполненой проверке:
        OEF проверка: {ci_OEF}
        Проверака расширений: {susp}
        Проверка с помощью VirusTotal": {vt_result['report_url']}""",
        str(report_path)
    }