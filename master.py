from pathlib import Path


# Проверка на скрытые данные в конце файла (EOF)
def check_image_EOF(file_path):
    signatures = [b'\xff\xd9', b'\x00\x00\x49\x45\x4e\x44\xae\x42\x60\x82']
    with open(file_path, 'rb') as f:
        content = f.read()
        for sig in signatures:
            if content.endswith(sig):
                return "Скрытые данные в конце изображения не обнаружены"
    return "Внимание: в файле обнаружен вредоносный код (подозрительный конец файла)"


# Проверка расширений
safe_suffixes = {'.png', '.jpg', '.jpeg', '.pdf'}

def is_suspicious(file_path):
    path = Path(file_path)
    suffixes = path.suffixes
    if len(suffixes) >= 2:
        return "Количество расширений не допустимо (двойные расширения)"
    last_suffix = path.suffix.lower()
    if last_suffix not in safe_suffixes:
        return "Расширение не безопасно"
    return "Расширение безопасно"