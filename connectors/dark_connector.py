import json

from datetime import datetime, timedelta
from model.entity.position import Position
from model.entity.song import Song
from model.repository.position_repository import PositionRepository
from model.repository.song_repository import SongRepository


def fill_db_chart(date: datetime):
	json_data = '''
[{"position": 1, "artists": "Kygo & Ava Max", "title": "Whatever", "external_id": "dht12"},{"position": 2, "artists": "Alok & Bebe Rexha", "title": "Deep In Your Love", "external_id": "dht6"},{"position": 3, "artists": "Alan Walker & Daya", "title": "Heart Over Mind", "external_id": "dht1"},{"position": 4, "artists": "Lufthaus & Robbie Williams feat. Sophie Ellis-Bextor ", "title": "Immortal", "external_id": "dht5"},{"position": 5, "artists": "Madison Beer", "title": "Make You Mine", "external_id": "dht28"},{"position": 6, "artists": "Robin Schulz & Topic feat. Oaks", "title": "One By One", "external_id": "dht3"},{"position": 7, "artists": "The Knocks & Sofi Tukker", "title": "One On One", "external_id": "dht10"},{"position": 8, "artists": "Mau P", "title": "Beats For The Underground", "external_id": "dht14"},{"position": 9, "artists": "Jax Jones & Zoe Wees", "title": "Never Be Lonely", "external_id": "dht23"},{"position": 10, "artists": "Seeb", "title": "Before You Go", "external_id": "dht50"},{"position": 11, "artists": "Eliza Rose & Calvin Harris", "title": "Body Moving", "external_id": "dht7"},{"position": 12, "artists": "Calvin Harris & Rag'n'Bone Man", "title": "Lovers In A Past Life", "external_id": "dht24"},{"position": 13, "artists": "Maggie Lindemann", "title": "Hostage", "external_id": "dht17"},{"position": 14, "artists": "Nero", "title": "Blame You", "external_id": "dht25"},{"position": 15, "artists": "Lucas Estrada, Tribbs & Stephen Puth", "title": "Close Your Eyes", "external_id": "dht45"},{"position": 16, "artists": "John Summit & Hayla", "title": "Shiver", "external_id": "dht36"},{"position": 17, "artists": "AURORA", "title": "Your Blood", "external_id": "dht8"},{"position": 18, "artists": "Leony", "title": "Simple Life", "external_id": "dht59"},{"position": 19, "artists": "PNAU & Empire of The Sun", "title": "AEIOU", "external_id": "dht2"},{"position": 20, "artists": "TDJ", "title": "Come Back Home", "external_id": "dht55"},{"position": 21, "artists": "Alle Farben & Maurice Lessing feat. Emma Wells", "title": "Dreams", "external_id": "dht51"},{"position": 22, "artists": "Tiësto, BIA & 21 Savage", "title": "Both", "external_id": "dht9"},{"position": 23, "artists": "Zerb & The Chainsmokers feat. Ink", "title": "Addicted", "external_id": "dht71"},{"position": 24, "artists": "Marshmello, P!nk & Sting", "title": "Dreaming", "external_id": "dht4"},{"position": 25, "artists": "Armin van Buuren & Goodboys", "title": "Forever (Stay Like This)", "external_id": "dht15"},{"position": 26, "artists": "Armin van Buuren & Gryffin", "title": "What Took You So Long", "external_id": "dht70"},{"position": 27, "artists": "Jubël feat. KIDDO", "title": "Lie To Me", "external_id": "dht16"},{"position": 28, "artists": "Wilkinson & Kelli-Leigh", "title": "This Moment", "external_id": "dht13"},{"position": 29, "artists": "Marshmello & Dove Cameron", "title": "Other Boys", "external_id": "dht18"},{"position": 30, "artists": "Galantis, David Guetta & 5 Seconds of Summer", "title": "Lighter", "external_id": "dht53"},{"position": 31, "artists": "Don Diablo, Major Lazer & Baby Lawd", "title": "Jiggy Woogie", "external_id": "dht64"},{"position": 32, "artists": "Sarah De Warren, Charming Horses & Hanno", "title": "This Is The Life", "external_id": "dht20"},{"position": 33, "artists": "Dimitri Vegas & Like Mike, Tiësto, W&W feat. Dido", "title": "Thank You (Not So Bad)", "external_id": "dht22"},{"position": 34, "artists": "Martin Garrix & Third Party feat. Oaks & Declan J Donovan", "title": "Carry You", "external_id": "dht31"},{"position": 35, "artists": "Justin Mylo & Karen Harding", "title": "Rescue Me", "external_id": "dht19"},{"position": 36, "artists": "Amél", "title": "Close To Me", "external_id": "dht58"},{"position": 37, "artists": "Kenya Grace", "title": "It's Not Fair", "external_id": "dht63"},{"position": 38, "artists": "Tiësto & Gabry Ponte", "title": "Mockingbird", "external_id": "dht75"},{"position": 39, "artists": "DVRST & polnalyubvi", "title": "Falling Stars", "external_id": "dht67"},{"position": 40, "artists": "Olivia Rodrigo", "title": "obsessed", "external_id": "dht68"},{"position": 41, "artists": "Justin Mylo & Ryos feat. SBSTN", "title": "In My Bones", "external_id": "dht61"},{"position": 42, "artists": "Campbell & Alcemist", "title": "Would You (go to bed with me)", "external_id": "dht69"},{"position": 43, "artists": "Teddy Swims", "title": "Lose Control (Tiësto Remix)", "external_id": "dht65"},{"position": 44, "artists": "Heidi Klum", "title": "Sunglasses at Night", "external_id": "dht56"},{"position": 45, "artists": "Martin Garrix, DubVision & Jaimes", "title": "Empty", "external_id": "dht62"},{"position": 46, "artists": "Lucas & Steve & LAWRENT feat. Jordan Shaw", "title": "End Of Time", "external_id": "dht74"},{"position": 47, "artists": "Sia & Kylie Minogue", "title": "Dance Alone (Ofenbach Remix)", "external_id": "dht73"},{"position": 48, "artists": "Felix Jaehn", "title": "Still Fall", "external_id": "dht35"},{"position": 49, "artists": "Tones And I", "title": "Dreaming", "external_id": "dht46"},{"position": 50, "artists": "Ava Max", "title": "My Oh My", "external_id": "dht72"}]
'''
	data = json.loads(json_data)
	chart_type = 'dark'

	if data:
		for song in data:
			external_id = song['external_id']
			position = song['position']
			song_object = SongRepository().get_song_by_ep_id(external_id)
			if not song_object:
				artists = song['artists']
				name = song['title']
				song_object = Song({
					'name': name,
					'authors': artists,
					'ep_id': external_id,
				})
				song_object = song_object.save()
			position_object = PositionRepository(chart_type).get_position_by_song_and_date(song_object.id, date)
			if position_object is None:
				position = Position({
					'position': position,
					'song_id': song_object.id,
					'chart_date': date,
					'chart_type': chart_type,
				})
				position = position.save()


if __name__ == '__main__':
	date_to_start = datetime(2024, 4, 12)
	fill_db_chart(date_to_start)


