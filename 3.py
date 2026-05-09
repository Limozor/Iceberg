import subprocess
from pathlib import Path

def zsteg_scan(file_path):
    try:
        res = subprocess.run(
            ['zsteg', file_path],
            capture_output=True, text=True, timeout=15
        )
        if res.returncode == 0:
            return res.stdout.strip() if res.stdout.strip() else "zsteg не обнаружил скрытых данных"
        else:
            return f"Ошибка zsteg: {res.stderr.strip()}"
    except Exception as e:
        return f"Ошибка: {e}"

test = zsteg_scan("test.png")
print(test)