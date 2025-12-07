from flask import Flask, render_template, request, jsonify, send_from_directory
import sys
import os

# Добавляем родительскую директорию в путь для импорта модулей
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model.repository.song_repository import song_repository
from db import database

app = Flask(__name__)

# Путь к папке с клипами
CLIPS_FOLDER = r'D:\Artyom\Проекты\Top Club Chart\клипы чарта\regulars'


@app.route('/')
def index():
	"""Главная страница со списком песен"""
	query = 'SELECT ID, AUTHORS, NAME, CLIP_PATH, EP_ID FROM songs WHERE CLIP_PATH IS NOT NULL AND CLIP_PATH != "" ORDER BY ID DESC LIMIT 100'
	songs = database.get_list(query)
	return render_template('clip_editor_index.html', songs=songs)


@app.route('/api/search')
def search_songs():
	"""API для поиска песен"""
	search_term = request.args.get('q', '').strip()

	if not search_term:
		query = 'SELECT ID, AUTHORS, NAME, CLIP_PATH, EP_ID FROM songs WHERE CLIP_PATH IS NOT NULL AND CLIP_PATH != "" ORDER BY ID DESC LIMIT 100'
		songs = database.get_list(query)
	else:
		# Поиск по ID, имени исполнителя или названию песни
		query = '''
			SELECT ID, AUTHORS, NAME, CLIP_PATH, EP_ID
			FROM songs 
			WHERE CLIP_PATH IS NOT NULL AND CLIP_PATH != ""
			AND (
				CAST(ID AS CHAR) LIKE %s
				OR LOWER(AUTHORS) LIKE %s
				OR LOWER(NAME) LIKE %s
			)
			ORDER BY ID DESC
			LIMIT 100
		'''
		search_pattern = f'%{search_term}%'
		songs = database.get_list(query, (search_pattern, search_pattern, search_pattern))

	return jsonify({'songs': songs})


@app.route('/editor/<int:song_id>')
def editor(song_id):
	"""Страница редактора для конкретной песни"""
	song = song_repository.get_song_by_id(song_id)
	if not song:
		return "Песня не найдена", 404

	return render_template('clip_editor.html', song=song)


@app.route('/api/song/<int:song_id>')
def get_song(song_id):
	"""API для получения данных песни"""
	song = song_repository.get_song_by_id(song_id)
	if not song:
		return jsonify({'error': 'Song not found'}), 404

	return jsonify({
		'id': song.id,
		'name': song.name,
		'authors': song.authors,
		'clip_path': song.clip_path,
		'clip_name': song.clip_name,
		'start_times': song.clip_start_sec,
		'end_times': song.clip_end_sec
	})


@app.route('/api/song/<int:song_id>/save', methods=['POST'])
def save_song_times(song_id):
	"""API для сохранения таймингов песни"""
	data = request.json
	start_times = data.get('start_times', [])
	end_times = data.get('end_times', [])

	# Валидация данных
	if len(start_times) != len(end_times):
		return jsonify({'error': 'Start and end times count mismatch'}), 400

	for i in range(len(start_times)):
		if start_times[i] >= end_times[i]:
			return jsonify({'error': f'Start time must be less than end time for segment {i+1}'}), 400

	# Формирование строк для БД
	start_times_str = ','.join([str(t) for t in start_times]) if start_times else None
	end_times_str = ','.join([str(t) for t in end_times]) if end_times else None

	# Обновление в БД
	query = 'UPDATE songs SET CLIP_START_SEC = %s, CLIP_END_SEC = %s WHERE ID = %s'
	database.execute_query(query, (start_times_str, end_times_str, song_id))

	return jsonify({'success': True, 'message': 'Times saved successfully'})


@app.route('/clips/<path:filename>')
def serve_clip(filename):
	"""Обслуживание видеофайлов из локальной папки"""
	return send_from_directory(CLIPS_FOLDER, filename)


if __name__ == '__main__':
	app.run(debug=True, host='127.0.0.1', port=5000)
