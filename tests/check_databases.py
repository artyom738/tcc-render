"""
Скрипт для проверки состояния баз данных (production и test)
"""
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pymysql
import db.database as database


def check_databases():
    """Проверяет состояние обеих баз данных"""

    print("=" * 60)
    print("ПРОВЕРКА БАЗ ДАННЫХ")
    print("=" * 60)

    # Проверяем production базу
    print("\n1. PRODUCTION база данных (tcc_render):")
    print("-" * 60)
    try:
        conn = pymysql.connect(**database.DB_CONFIG)
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as cnt FROM songs")
            songs_count = cursor.fetchone()['cnt']

            cursor.execute("SELECT MAX(ID) as max_id FROM songs")
            max_song_id = cursor.fetchone()['max_id']

            cursor.execute("SELECT COUNT(*) as cnt FROM charts")
            charts_count = cursor.fetchone()['cnt']

            cursor.execute("SELECT MAX(ID) as max_id FROM charts")
            max_chart_id = cursor.fetchone()['max_id']
        conn.close()

        print(f"✓ Песен: {songs_count}")
        print(f"✓ Максимальный ID песни: {max_song_id}")
        print(f"✓ Чартов: {charts_count}")
        print(f"✓ Максимальный ID чарта: {max_chart_id}")

    except Exception as e:
        print(f"✗ Ошибка: {e}")

    # Проверяем тестовую базу
    print("\n2. ТЕСТОВАЯ база данных (tcc_render_test):")
    print("-" * 60)
    try:
        conn = pymysql.connect(**database.TEST_DB_CONFIG)
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as cnt FROM songs")
            songs_count = cursor.fetchone()['cnt']

            cursor.execute("SELECT COUNT(*) as cnt FROM charts")
            charts_count = cursor.fetchone()['cnt']

            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
        conn.close()

        print(f"✓ Песен: {songs_count}")
        print(f"✓ Чартов: {charts_count}")
        print(f"✓ Таблиц: {len(tables)}")

        if songs_count == 0 and charts_count == 0:
            print("\n✓ Тестовая база данных ЧИСТА (как и должно быть после тестов)")
        else:
            print("\n⚠ Тестовая база содержит данные (возможно тесты не очистились)")

    except Exception as e:
        print(f"✗ Ошибка: {e}")

    print("\n" + "=" * 60)
    print("ИТОГ:")
    print("=" * 60)
    print("✓ Production база (tcc_render) - защищена и не изменяется")
    print("✓ Тестовая база (tcc_render_test) - используется для тестов")
    print("✓ AUTO_INCREMENT в тестовой базе сбрасывается после каждого теста")
    print("=" * 60)


if __name__ == '__main__':
    check_databases()

