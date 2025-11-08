import unittest
import os
import sys

# Ensure tests directory is on sys.path so we can import db_test_utils without colliding with top-level tests.py
sys.path.insert(0, os.path.dirname(__file__))
from db_test_utils import transactional
from model.repository.song_repository import SongRepository


class TestSongRepository(unittest.TestCase):
    def setUp(self):
        self.repo = SongRepository()

    def test_fetch_object_creates_song_object(self):
        # Проверяем, что fetch_object корректно мапит словарь в объект Song
        data = {
            'ID': 1,
            'NAME': 'Test Song',
            'AUTHORS': 'Test Author',
            'EP_ID': 'EP999',
            'ORIGINAL_ID': None,
            'CLIP_PATH': 'test.mp4',
            'CLIP_START_SEC': 10,
            'CLIP_END_SEC': 40,
        }
        song = self.repo.fetch_object(data)
        self.assertEqual(song.id, 1)
        self.assertEqual(song.name, 'Test Song')
        self.assertEqual(song.authors, 'Test Author')
        self.assertEqual(song.ep_id, 'EP999')
        self.assertEqual(song.clip_name, 'test.mp4')
        self.assertTrue(song.clip_path.endswith('test.mp4'))
        # clip_start_sec and clip_end_sec are lists of floats
        self.assertIsInstance(song.clip_start_sec, list)
        self.assertIsInstance(song.clip_end_sec, list)
        self.assertEqual(song.clip_start_sec[0], 10.0)
        self.assertEqual(song.clip_end_sec[0], 40.0)

    def test_get_song_by_id_with_transaction(self):
        # Интеграционный тест: создаём строку в songs внутри тестовой базы
        with transactional():
            import pymysql
            import db.database as database

            connection = pymysql.connect(**database.get_db_config())
            try:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO songs (ID, NAME, AUTHORS, EP_ID, ORIGINAL_ID, CLIP_PATH, CLIP_START_SEC, CLIP_END_SEC) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                        (100, 'Transactional Song', 'Tx Author', 'EP-TX-1', None, 'tx_clip.mp4', '5', '30')
                    )
                connection.commit()
            finally:
                connection.close()

            # Теперь вызовем репозиторий для получения песни из тестовой БД
            song = self.repo.get_song_by_id(100)
            self.assertIsNotNone(song)
            self.assertEqual(song.id, 100)
            self.assertEqual(song.name, 'Transactional Song')


if __name__ == '__main__':
    unittest.main()
