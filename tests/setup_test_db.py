"""
Скрипт для инициализации тестовой базы данных.
Запустите этот скрипт один раз перед запуском тестов.
"""

import sys
from pathlib import Path

# Добавляем корень проекта в sys.path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Добавляем директорию tests в sys.path
tests_dir = Path(__file__).parent
sys.path.insert(0, str(tests_dir))

from db_test_utils import setup_test_database, teardown_test_database

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Управление тестовой базой данных')
    parser.add_argument('action', choices=['setup', 'teardown', 'recreate'],
                       help='setup - создать БД, teardown - удалить БД, recreate - пересоздать БД')

    args = parser.parse_args()

    if args.action == 'setup':
        print("Создание тестовой базы данных...")
        setup_test_database()
    elif args.action == 'teardown':
        print("Удаление тестовой базы данных...")
        teardown_test_database()
    elif args.action == 'recreate':
        print("Пересоздание тестовой базы данных...")
        teardown_test_database()
        setup_test_database()

    print("\nГотово!")
