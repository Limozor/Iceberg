import os
from PIL import Image
from PIL.ExifTags import TAGS

# Списки для проверки
NORMAL_TAGS = {
    'Make', 'Model', 'DateTime', 'ExposureTime', 'FNumber', 'ISOSpeedRatings',
    'ShutterSpeedValue', 'ApertureValue', 'BrightnessValue', 'ExposureBiasValue',
    'MaxApertureValue', 'MeteringMode', 'LightSource', 'Flash', 'FocalLength',
    'ColorSpace', 'ExifImageWidth', 'ExifImageHeight', 'Orientation', 'Software',
    'Artist', 'Copyright', 'GPSInfo', 'LensModel', 'LensMake', 'SceneType',
    'WhiteBalance', 'DigitalZoomRatio', 'Contrast', 'Saturation', 'Sharpness',
    "ImageWidth", "39424", "ImageLength", "34979", "34970", "ResolutionUnit",
    "ExifOffset", "YCbCrPositioning", "39321", "XResolution", "YResolution",
    "34973", "ExifVersion", "DateTimeOriginal", "FlashPixVersion", "SubsecTime",
    "ComponentsConfiguration", "OffsetTime","ExifInteroperabilityOffset",
    "SubsecTimeOriginal", "SubsecTimeDigitized", "OffsetTimeOriginal", "34965",
    "DateTimeDigitized", "SensingMethod", "34974", "34975", "ExposureProgram",
    "ExposureMode", "SensitivityType", "ISOSpeed", "FocalLengthIn35mmFilm",
    "42593", "MakerNote" "39424", "34979", "34970", "39321", "34973", "34965",
    "34974", "34975", "42593"
}

SUSPICIOUS_KEYWORDS = [
    'script', 'eval', 'base64', 'exec', 'cmd', 'powershell', '<?php', '<script',
    'javascript', 'vbscript', 'onload', 'onerror', 'alert', 'window.location'
]

SUSPICIOUS_TAGS = [
    'ImageDescription', 'Artist', 'Copyright', 'UserComment',
    'XPTitle', 'XPComment', 'XPKeywords', 'XPSubject'
]


def check_photo_anomalies(file_path):
    """
    Проверяет фото на аномалии EXIF.
    Возвращает строку с отчётом или None, если аномалий нет.
    """
    # 1. Пытаемся открыть и прочитать EXIF
    try:
        with Image.open(file_path) as img:
            raw_exif = img._getexif()
    except Exception as e:
        return f"❌ Ошибка при открытии '{file_path}': {e}"

    # 2. Если EXIF нет
    if not raw_exif:
        return None  # нет данных то нет аномалий

    # 3. Преобразуем EXIF в читаемый словарь
    exif_dict = {}
    for tag_id, value in raw_exif.items():
        tag_name = TAGS.get(tag_id, tag_id)
        exif_dict[tag_name] = value

    # 5. Ищем аномалии
    anomalies = []

    # Нестандартные теги
    for tag in exif_dict.keys():
        if tag not in NORMAL_TAGS:
            anomalies.append(f"🔍 Нестандартный тег: {tag}")

    # Подозрительный контент
    for tag in SUSPICIOUS_TAGS:
        if tag in exif_dict:
            value = str(exif_dict[tag]).lower()
            for kw in SUSPICIOUS_KEYWORDS:
                if kw in value:
                    anomalies.append(f"⚠️ Подозрительный контент в теге {tag}: {value[:100]}")
                    break

    # Слишком много тегов
    if len(exif_dict) > 80:
        anomalies.append(f"📦 Необычно много EXIF-тегов: {len(exif_dict)}")

    # GPS
    if 'GPSInfo' in exif_dict:
        anomalies.append("📍 Обнаружены GPS-координаты")

    # 6. Формируем результат
    if not anomalies:
        return "Аномалии не обнаружены"

    result_lines = [f"🚨 Файл: {file_path}"]
    result_lines.extend(f"   {a}" for a in anomalies)
    return "\n".join(result_lines)
