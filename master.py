from pathlib import Path


# Проверка на скрытые данные в конце файла (EOF)
def check_image_EOF(file_path):
    # Размеры сигнатур концов файлов (JPG, PNG)
    signatures = [b'\xff\xd9', b'\x00\x00\x49\x45\x4e\x44\xae\x42\x60\x82']

    with open(file_path, 'rb') as f:
        content = f.read()
        check_EOF = "Внимание в конце файла обнаружен вредоносный код"
        for sig in signatures:
            if content.endswith(sig):
                check_EOF = "Скрытые данные в конце изображения не обнаружены"
                break
    return check_EOF


# Проверка расширений
safe_suffixes = {'.png', '.jpg', '.jpeg', '.pdf'}
def is_suspicious(file_path):
    path = Path(file_path)
    suffixes = path.suffixes
    if len(suffixes) >= 2:
        return "Количество расширений не допустимо"
    last_suffix = path.suffix.lower()
    if last_suffix not in safe_suffixes:
        return "Расширение не безопастно"
    return "Файл прошел проверку на расширения"


# Активация функций проверки
check_suffixes = is_suspicious("тесты/test.jpg") # Расширения
check_EOF = check_image_EOF("тесты/test.exe") # Только .jpg и .png

print(check_suffixes, check_EOF, sep="\n") # Вывод в терминал результы тестов