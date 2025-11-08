# Один раз создать тестовую БД
python tests\setup_test_db.py setup

# Запустить все тесты
python -m unittest discover tests -v

# Проверить состояние баз данных
python tests\check_databases.py