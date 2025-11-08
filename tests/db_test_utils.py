import pymysql
import os
import sys
from pathlib import Path

# Добавляем корень проекта в sys.path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import db.database as database


def setup_test_database():
    """Создает и инициализирует тестовую базу данных"""
    # Подключаемся без указания базы данных для создания новой
    conn = pymysql.connect(
        host=database.TEST_DB_CONFIG['host'],
        user=database.TEST_DB_CONFIG['user'],
        password=database.TEST_DB_CONFIG['password'],
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with conn.cursor() as cursor:
            # Создаем тестовую базу данных
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{database.TEST_DB_CONFIG['database']}` "
                         "CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci")
            cursor.execute(f"USE `{database.TEST_DB_CONFIG['database']}`")

            # Читаем и выполняем SQL схему
            install_sql_path = project_root / 'db' / 'install.sql'
            with open(install_sql_path, 'r', encoding='utf-8') as f:
                sql_content = f.read()

            # Разбиваем на отдельные команды и выполняем
            # Пропускаем CREATE DATABASE и USE команды из install.sql
            statements = []
            current_statement = []

            for line in sql_content.split('\n'):
                line = line.strip()
                # Пропускаем комментарии и пустые строки
                if not line or line.startswith('--'):
                    continue
                # Пропускаем CREATE DATABASE и USE
                if line.startswith('CREATE DATABASE') or line.startswith('USE '):
                    continue

                current_statement.append(line)
                if line.endswith(';'):
                    stmt = ' '.join(current_statement)
                    if stmt.strip():
                        statements.append(stmt)
                    current_statement = []

            # Выполняем каждую команду
            for stmt in statements:
                if stmt.strip():
                    cursor.execute(stmt)

        conn.commit()
        print(f"✓ Тестовая база данных '{database.TEST_DB_CONFIG['database']}' успешно создана и инициализирована")

    finally:
        conn.close()


def teardown_test_database():
    """Удаляет тестовую базу данных"""
    conn = pymysql.connect(
        host=database.TEST_DB_CONFIG['host'],
        user=database.TEST_DB_CONFIG['user'],
        password=database.TEST_DB_CONFIG['password'],
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with conn.cursor() as cursor:
            cursor.execute(f"DROP DATABASE IF EXISTS `{database.TEST_DB_CONFIG['database']}`")
        conn.commit()
        print(f"✓ Тестовая база данных '{database.TEST_DB_CONFIG['database']}' удалена")
    finally:
        conn.close()


def clean_test_database():
    """Очищает все таблицы в тестовой базе данных"""
    conn = pymysql.connect(**database.TEST_DB_CONFIG)

    try:
        with conn.cursor() as cursor:
            # Отключаем проверку внешних ключей
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

            # Получаем список всех таблиц
            cursor.execute(f"SHOW TABLES")
            tables = cursor.fetchall()

            # Очищаем каждую таблицу
            for table_dict in tables:
                table_name = list(table_dict.values())[0]
                cursor.execute(f"TRUNCATE TABLE `{table_name}`")

            # Включаем проверку внешних ключей обратно
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

        conn.commit()

    finally:
        conn.close()


def use_test_database():
    """Включает режим использования тестовой базы данных"""
    os.environ['TCC_TEST_MODE'] = '1'


def use_production_database():
    """Возвращает использование production базы данных"""
    if 'TCC_TEST_MODE' in os.environ:
        del os.environ['TCC_TEST_MODE']


class TestDatabaseContext:
    """Контекстный менеджер для работы с тестовой базой данных"""

    def __enter__(self):
        use_test_database()
        clean_test_database()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        clean_test_database()
        use_production_database()


# Для обратной совместимости со старыми тестами
# (но теперь это использует отдельную тестовую БД)
def transactional():
    """Использует тестовую базу данных вместо транзакций"""
    return TestDatabaseContext()
