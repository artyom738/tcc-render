import pymysql.cursors

DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',
    'database': 'tcc_render',
    'cursorclass': pymysql.cursors.DictCursor,
    'autocommit': True
}


def get_cursor():
    """Возвращает курсор без указания базы данных."""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        return connection.cursor()
    except Exception as e:
        print("Error connecting to database:", e)
        return None


def execute_query(sql, params=None):
    """Выполняет SQL-запрос и возвращает результат."""
    try:
        connection = pymysql.connect(**DB_CONFIG)
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
        connection = pymysql.connect(**DB_CONFIG)
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
        connection = pymysql.connect(**DB_CONFIG)
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            last_id = cursor.lastrowid
        connection.close()
        return last_id
    except Exception as e:
        print("Error executing insert:", sql)
        print("Error text:", str(e))
        return None

