#!/usr/bin/env python
"""
Скрипт для запуска тестов с генерацией отчета о покрытии
"""

import os
import sys
import subprocess
import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    django.setup()

    # Запуск тестов с coverage
    print("Запуск тестов с покрытием...")

    # Команда для запуска coverage
    cmd = ["coverage", "run", "--source=.", "manage.py", "test", "tests"]

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("Тесты выполнены успешно!")
        print(result.stdout)

        # Генерация HTML отчета
        print("\nГенерация HTML отчета...")
        html_cmd = ["coverage", "html"]
        html_result = subprocess.run(
            html_cmd, check=True, capture_output=True, text=True
        )
        print("HTML отчет создан в директории htmlcov/")

        # Показать краткий отчет в консоли
        print("\nКраткий отчет о покрытии:")
        report_cmd = ["coverage", "report"]
        report_result = subprocess.run(
            report_cmd, check=True, capture_output=True, text=True
        )
        print(report_result.stdout)

    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении тестов: {e}")
        print(f"Вывод: {e.stdout}")
        print(f"Ошибки: {e.stderr}")
        sys.exit(1)
    except FileNotFoundError:
        print(
            "Ошибка: coverage не установлен. Установите его командой: pip install coverage"
        )
        sys.exit(1)
