from pathlib import Path
from VirusTotal import VT_report


# Проверка на скрытые данные в конце файла (EOF)
def check_image_EOF(master_file):
    signatures = [b'\xff\xd9', b'\x00\x00\x49\x45\x4e\x44\xae\x42\x60\x82']
    with open(master_file, 'rb') as f:
        content = f.read()
        for sig in signatures:
            if content.endswith(sig):
                return ""
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
    ci_OEF = check_image_EOF(file_path)
    susp = is_suspicious(file_path)
    vt_result = VT_report(file_path)

    return {
        "OEF проверка": ci_OEF,
        "Проверака расширений": susp,
        "Проверка с помощью VirusTotal": vt_result['report_url']
    }