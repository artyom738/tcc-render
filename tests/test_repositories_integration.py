"""
Комплексные интеграционные тесты для репозиториев
Все тесты используют отдельную тестовую базу данных tcc_render_test
"""
import unittest
import os
import sys
import datetime

sys.path.insert(0, os.path.dirname(__file__))
from db_test_utils import transactional
from model.repository.song_repository import SongRepository
from model.repository.chart_repository import ChartRepository


class TestSongRepositoryIntegration(unittest.TestCase):
    """Интеграционные тесты для SongRepository"""

    def setUp(self):
        self.repo = SongRepository()

    def test_add_and_retrieve_song(self):
        """Тест добавления и получения песни"""
        with transactional():
            import pymysql
            import db.database as database

            conn = pymysql.connect(**database.get_db_config())
            try:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO songs (NAME, AUTHORS, EP_ID, CLIP_PATH, CLIP_START_SEC, CLIP_END_SEC) "
                        "VALUES (%s, %s, %s, %s, %s, %s)",
                        ('Test Song 1', 'Test Author 1', 'EP-TEST-001', 'test1.mp4', '10', '40')
                    )
                    song_id = cursor.lastrowid
                conn.commit()
            finally:
                conn.close()

            # Получаем песню
            song = self.repo.get_song_by_id(song_id)
            self.assertIsNotNone(song)
            self.assertEqual(song.name, 'Test Song 1')
            self.assertEqual(song.authors, 'Test Author 1')
            self.assertEqual(song.ep_id, 'EP-TEST-001')

    def test_get_song_by_ep_id(self):
        """Тест получения песни по EP_ID"""
        with transactional():
            import pymysql
            import db.database as database

            conn = pymysql.connect(**database.get_db_config())
            try:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO songs (NAME, AUTHORS, EP_ID) VALUES (%s, %s, %s)",
                        ('Song By EP', 'EP Author', 'EP-UNIQUE-999')
                    )
                conn.commit()
            finally:
                conn.close()

            song = self.repo.get_song_by_ep_id('EP-UNIQUE-999')
            self.assertIsNotNone(song)
            self.assertEqual(song.name, 'Song By EP')

    def test_get_songs_with_no_clips(self):
        """Тест получения песен без клипов"""
        with transactional():
            import pymysql
            import db.database as database

            conn = pymysql.connect(**database.get_db_config())
            try:
                with conn.cursor() as cursor:
                    # Песня с клипом
                    cursor.execute(
                        "INSERT INTO songs (NAME, AUTHORS, EP_ID, CLIP_PATH) VALUES (%s, %s, %s, %s)",
                        ('Song With Clip', 'Author 1', 'EP-1', 'clip1.mp4')
                    )
                    # Песня без клипа
                    cursor.execute(
                        "INSERT INTO songs (NAME, AUTHORS, EP_ID, CLIP_PATH) VALUES (%s, %s, %s, %s)",
                        ('Song Without Clip', 'Author 2', 'EP-2', None)
                    )
                    # Еще одна песня без клипа (пустая строка)
                    cursor.execute(
                        "INSERT INTO songs (NAME, AUTHORS, EP_ID, CLIP_PATH) VALUES (%s, %s, %s, %s)",
                        ('Song Empty Clip', 'Author 3', 'EP-3', '')
                    )
                conn.commit()
            finally:
                conn.close()

            songs_no_clips = self.repo.get_songs_with_no_clips()
            self.assertEqual(len(songs_no_clips), 2)
            names = [s.name for s in songs_no_clips]
            self.assertIn('Song Without Clip', names)
            self.assertIn('Song Empty Clip', names)


class TestChartRepositoryIntegration(unittest.TestCase):
    """Интеграционные тесты для ChartRepository"""

    def setUp(self):
        self.repo = ChartRepository()

    def test_add_and_retrieve_chart(self):
        """Тест добавления и получения чарта"""
        with transactional():
            import pymysql
            import db.database as database

            conn = pymysql.connect(**database.get_db_config())
            try:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO charts (CHART_TYPE, CHART_NUMBER, CHART_DATE) VALUES (%s, %s, %s)",
                        ('tcc', 100, datetime.date(2025, 1, 1))
                    )
                    chart_id = cursor.lastrowid
                conn.commit()
            finally:
                conn.close()

            chart = self.repo.get_chart_by_id(chart_id)
            self.assertIsNotNone(chart)
            self.assertEqual(chart.chart_type, 'tcc')
            self.assertEqual(chart.chart_number, 100)

    def test_get_last_chart_by_type(self):
        """Тест получения последнего чарта по типу"""
        with transactional():
            import pymysql
            import db.database as database

            conn = pymysql.connect(**database.get_db_config())
            try:
                with conn.cursor() as cursor:
                    # Добавляем несколько чартов разных типов и дат
                    cursor.execute(
                        "INSERT INTO charts (CHART_TYPE, CHART_NUMBER, CHART_DATE) VALUES (%s, %s, %s)",
                        ('tcc', 1, datetime.date(2025, 1, 1))
                    )
                    cursor.execute(
                        "INSERT INTO charts (CHART_TYPE, CHART_NUMBER, CHART_DATE) VALUES (%s, %s, %s)",
                        ('tcc', 2, datetime.date(2025, 1, 8))
                    )
                    cursor.execute(
                        "INSERT INTO charts (CHART_TYPE, CHART_NUMBER, CHART_DATE) VALUES (%s, %s, %s)",
                        ('darknity', 1, datetime.date(2025, 1, 5))
                    )
                conn.commit()
            finally:
                conn.close()

            last_tcc = self.repo.get_last_chart_by_type('tcc')
            self.assertIsNotNone(last_tcc)
            self.assertEqual(last_tcc.chart_number, 2)
            self.assertEqual(last_tcc.chart_date, datetime.date(2025, 1, 8))

    def test_get_previous_chart(self):
        """Тест получения предыдущего чарта"""
        with transactional():
            import pymysql
            import db.database as database

            conn = pymysql.connect(**database.get_db_config())
            try:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO charts (CHART_TYPE, CHART_NUMBER, CHART_DATE) VALUES (%s, %s, %s)",
                        ('tcc', 10, datetime.date(2025, 1, 1))
                    )
                    first_id = cursor.lastrowid
                    cursor.execute(
                        "INSERT INTO charts (CHART_TYPE, CHART_NUMBER, CHART_DATE) VALUES (%s, %s, %s)",
                        ('tcc', 11, datetime.date(2025, 1, 8))
                    )
                    second_id = cursor.lastrowid
                conn.commit()
            finally:
                conn.close()

            previous = self.repo.get_previous_chart(second_id)
            self.assertIsNotNone(previous)
            self.assertEqual(previous.id, first_id)
            self.assertEqual(previous.chart_number, 10)


class TestChartPositionsIntegration(unittest.TestCase):
    """Интеграционные тесты для работы с позициями в чарте"""

    def test_full_chart_workflow(self):
        """Полный тест создания чарта с позициями"""
        with transactional():
            import pymysql
            import db.database as database

            conn = pymysql.connect(**database.get_db_config())
            try:
                with conn.cursor() as cursor:
                    # Создаем песни
                    songs = []
                    for i in range(1, 6):
                        cursor.execute(
                            "INSERT INTO songs (NAME, AUTHORS, EP_ID) VALUES (%s, %s, %s)",
                            (f'Song {i}', f'Author {i}', f'EP-{i}')
                        )
                        songs.append(cursor.lastrowid)

                    # Создаем чарт
                    cursor.execute(
                        "INSERT INTO charts (CHART_TYPE, CHART_NUMBER, CHART_DATE) VALUES (%s, %s, %s)",
                        ('tcc', 999, datetime.date.today())
                    )
                    chart_id = cursor.lastrowid

                    # Добавляем позиции
                    for pos, song_id in enumerate(songs, 1):
                        cursor.execute(
                            "INSERT INTO chart_positions (CHART_ID, SONG_ID, POSITION) VALUES (%s, %s, %s)",
                            (chart_id, song_id, pos)
                        )
                conn.commit()
            finally:
                conn.close()

            # Проверяем что все создано
            cursor = database.get_cursor()
            cursor.execute(f"SELECT COUNT(*) as cnt FROM chart_positions WHERE CHART_ID = {chart_id}")
            result = cursor.fetchone()
            self.assertEqual(result['cnt'], 5)

    def test_auto_increment_reset_between_tests(self):
        """Проверяем что AUTO_INCREMENT сбрасывается между тестами"""
        with transactional():
            import pymysql
            import db.database as database

            conn = pymysql.connect(**database.get_db_config())
            try:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO songs (NAME, AUTHORS, EP_ID) VALUES (%s, %s, %s)",
                        ('First Song', 'First Author', 'EP-FIRST')
                    )
                    first_id = cursor.lastrowid
                conn.commit()
            finally:
                conn.close()

            # ID должен быть маленьким (не миллионы), так как база очищается
            self.assertLess(first_id, 1000,
                          f"AUTO_INCREMENT не сброшен! ID = {first_id}")


if __name__ == '__main__':
    unittest.main()

