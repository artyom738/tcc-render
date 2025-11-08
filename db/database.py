import pymysql.cursors
import os

DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',
    'database': 'tcc_render',
    'cursorclass': pymysql.cursors.DictCursor,
    'autocommit': True
}

# Конфигурация для тестовой базы данных
TEST_DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',
    'database': 'tcc_render_test',
    'cursorclass': pymysql.cursors.DictCursor,
    'autocommit': True
}


# Переменная окружения для переключения на тестовую БД
def get_db_config():
    """Возвращает конфигурацию БД в зависимости от режима (prod/test)"""
    if os.environ.get('TCC_TEST_MODE') == '1':
        return TEST_DB_CONFIG
    return DB_CONFIG


def get_cursor():
    """Возвращает курсор без указания базы данных."""
    try:
        connection = pymysql.connect(**get_db_config())
        return connection.cursor()
    except Exception as e:
        print("Error connecting to database:", e)
        return None


def execute_query(sql, params=None):
    """Выполняет SQL-запрос и возвращает результат."""
    try:
        connection = pymysql.connect(**get_db_config())
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            result = cursor.fetchall()
        connection.close()
        return result
    except Exception as e:
        print("Error executing query:", sql)
        print("Error text:", str(e))
        return []


def get_list(sql, params=None):
    """Возвращает список словарей по SQL-запросу."""
    try:
        connection = pymysql.connect(**get_db_config())
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            result = cursor.fetchall()
        connection.close()
        return result
    except Exception as e:
        print("Error executing query:", sql)
        print("Error text:", str(e))
        return []


def add(sql, params):
    """Выполняет INSERT и возвращает lastrowid."""
    try:
        connection = pymysql.connect(**get_db_config())
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            last_id = cursor.lastrowid
        connection.close()
        return last_id
    except Exception as e:
        print("Error executing insert:", sql)
        print("Error text:", str(e))
        return None
