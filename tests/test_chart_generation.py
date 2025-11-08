import unittest
import os
import sys
import datetime

# Ensure tests directory is on sys.path so we can import db_test_utils without colliding with top-level tests.py
sys.path.insert(0, os.path.dirname(__file__))
from db_test_utils import transactional
from model.repository.chart_repository import ChartRepository
from charts.base_chart import BaseChart


class TestChartGeneration(unittest.TestCase):
    def test_create_chart_and_position_transactional(self):
        with transactional():
            import pymysql
            import db.database as database

            connection = pymysql.connect(**database.get_db_config())
            try:
                with connection.cursor() as cursor:
                    # Вставим тестовую песню
                    cursor.execute(
                        "INSERT INTO songs (ID, NAME, AUTHORS, EP_ID, CLIP_PATH, CLIP_START_SEC, CLIP_END_SEC) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (1, 'ChartSong Tx', 'Chart Author', 'EP-CH-1', 'chart_tx.mp4', '1', '20')
                    )
                    # Вставим тестовый чарт
                    cursor.execute(
                        "INSERT INTO charts (ID, CHART_TYPE, CHART_NUMBER, CHART_DATE) "
                        "VALUES (%s, %s, %s, %s)",
                        (1, 'tcc', 9999, datetime.date.today())
                    )
                    # Вставим позицию
                    cursor.execute(
                        "INSERT INTO chart_positions (CHART_ID, SONG_ID, POSITION) VALUES (%s, %s, %s)",
                        (1, 1, 1)
                    )
                connection.commit()
            finally:
                connection.close()

            # Получаем чарт через репозиторий — теперь он использует тестовую БД
            repo = ChartRepository()
            chart = repo.get_chart_by_id(1)
            self.assertIsNotNone(chart)
            self.assertEqual(chart.id, 1)
            self.assertEqual(chart.chart_type, 'tcc')

            # Создадим BaseChart и проверим некоторые методы (без реального рендера)
            base = BaseChart(chart)
            # get_chart_type в BaseChart не реализован
            with self.assertRaises(NotImplementedError):
                base.get_chart_type()
            # get_last_out_composition default empty list
            self.assertEqual(base.get_last_out_composition(), [])


if __name__ == '__main__':
    unittest.main()
