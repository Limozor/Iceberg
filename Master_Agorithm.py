#Каз,нел пом
import random
from pathlib import Path
from pythonping import ping
from EXIF import Check_EXIF
from VirusTotal import Virus_Total_Scan
from Algorithms import Check_General, Check_EOF, Cheak_Suspicious



def Processing_Report(file_path):
    Check_General_res = Check_General(file_path)
    Cheak_Suspicious_res = Cheak_Suspicious(file_path)
    Check_EOF_res = Check_EOF(file_path)
    Check_EXIF_res = Check_EXIF(file_path)

    List_Checks = [Check_General_res, Cheak_Suspicious_res, Check_EOF_res, Check_EXIF_res]

    Report_UNSAFE = []
    Report_ODD = []

    if ping("virustotal.com").success():
        VirusTotal_Universal_res = Virus_Total_Scan(file_path)
        if VirusTotal_Universal_res[1] == True:
            Report_UNSAFE.extend(VirusTotal_Universal_res[3:])
        elif VirusTotal_Universal_res[2] == True:
            Report_ODD.extend(VirusTotal_Universal_res[3:])

    for lst in List_Checks:
        first_unit, second_unit = lst[0], lst[1]
        if first_unit:
            Report_UNSAFE.extend(lst[2:])
        elif second_unit:
            Report_ODD.extend(lst[2:])

    flag = False
    if (not Report_UNSAFE) and (not Report_ODD): # Списки пустые и файл безопасен
        flag = True
        report_file_data = f"""🧊 Сканирование завершено. Файл чист.
Проверка проведена по всем актуальным базам и алгоритмам Айсберга. Вредоносная активность не выявлена. Доступ к содержимому безопасен. 💙"""
        REPORT = f"""🧊 Сканирование завершено. Файл чист.
Проверка проведена по всем актуальным базам и алгоритмам Айсберга. Вредоносная активность не выявлена. Доступ к содержимому безопасен. 💙"""

    elif Report_ODD and flag == False :
        flag = True
        report_file_data = "\n".join(Report_UNSAFE)
        REPORT = f"""ВНИМАНИЕ 
⚠ ФАЙЛ ПОДОЗРИТЕЛЬНЫЙ ⚠
{"\n".join(Report_ODD)}
"""

    elif Report_UNSAFE and flag == False:
        report_file_data = "\n".join(Report_UNSAFE)
        REPORT = f"""ВНИМАНИЕ
‼ ФАЙЛ ОПАСЕН ‼
{"\n".join(Report_UNSAFE)}
"""

    report_dir = Path("reports")
    report_dir.mkdir(parents=True, exist_ok=True)
    base_name = Path(file_path).stem
    random_num = random.randint(100, 999)
    report_filename = f"Report_{base_name}_{random_num}.txt"
    report_path = report_dir / report_filename
    report_path.write_text(report_file_data, encoding="utf-8")

    return (REPORT, str(report_path))
