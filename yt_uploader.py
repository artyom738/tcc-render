import httplib2
import os
import random
import sys
import time

from types import SimpleNamespace
from apiclient.discovery import build
from apiclient.errors import HttpError
from apiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow

import yt_description

from model.entity.chart import Chart
from model.repository.chart_repository import chart_repository

httplib2.RETRIES = 1

# Maximum number of times to retry before giving up.
MAX_RETRIES = 10

# Always retry when these exceptions are raised.
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError)

# Always retry when an apiclient.errors.HttpError with one of these status
# codes is raised.
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

CLIENT_SECRETS_FILE = "yt_credentials.json"
YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")

class YTUploader:
	def get_authenticated_service(self, args):
		flow = flow_from_clientsecrets(
			CLIENT_SECRETS_FILE,
			scope=YOUTUBE_UPLOAD_SCOPE,
			message='OAuth has never been set up'
		)
		storage = Storage("%s-oauth2.json" % sys.argv[0])
		credentials = storage.get()

		if credentials is None or credentials.invalid:
			credentials = run_flow(flow, storage, args)

		return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, http=credentials.authorize(httplib2.Http()))

	def initialize_upload(self, youtube, options):
		tags = None
		if options.keywords:
			tags = options.keywords.split(",")

		body = {
			'snippet': {
				'title': options.title,
				'description': options.description,
				'tags': tags,
				'categoryId': options.category,
			},
			'status': {
				'privacyStatus': options.privacyStatus,
			}
		}

		insert_request = youtube.videos().insert(
			part=",".join(body.keys()),
			body=body,
			media_body=MediaFileUpload(options.file, chunksize=-1, resumable=True)
		)

		return self.resumable_upload(insert_request)

	def resumable_upload(self, insert_request):
		response = None
		error = None
		retry = 0
		while response is None:
			try:
				print("Uploading file...")
				status, response = insert_request.next_chunk()
				if response is not None:
					if 'id' in response:
						print("Video id '%s' was successfully uploaded." % response['id'])
						return response['id']
					else:
						exit("The upload failed with an unexpected response: %s" % response)
			except HttpError as e:
				if e.resp.status in RETRIABLE_STATUS_CODES:
					error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
				else:
					raise
			except RETRIABLE_EXCEPTIONS as e:
				error = "A retriable error occurred: %s" % e

			if error is not None:
				print(error)
				retry += 1
				if retry > MAX_RETRIES:
					exit("No longer attempting to retry.")

				max_sleep = 2 ** retry
				sleep_seconds = random.random() * max_sleep
				print("Sleeping %f seconds and then retrying..." % sleep_seconds)
				time.sleep(sleep_seconds)

	def upload_video(self, chart: Chart):
		filename = f'production/{chart.chart_type} {chart.chart_date.strftime("%Y-%m-%d")}.mp4'
		args = SimpleNamespace(
			file=filename,
			title=yt_description.get_yt_title(chart),
			description=yt_description.get_yt_description(chart),
			category='10',
			keywords=yt_description.get_tags(chart),
			privacyStatus='private',
			logging_level='DEBUG',
			noauth_local_webserver=None,
			auth_host_port=[],
		)
		if not os.path.exists(args.file):
			exit('YTUploader: file path is invalid')
		youtube = self.get_authenticated_service(args)
		try:
			video_id = self.initialize_upload(youtube, args)
			self.upload_thumbnail(youtube, video_id, chart)
		except HttpError as e:
			print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))

	def upload_thumbnail(self, youtube, video_id: str, chart: Chart):
		print('Uploading thumbnail...')
		file_path = f'previews/preview_{chart.chart_type}_{chart.chart_number}.png'
		youtube.thumbnails().set(
			videoId=video_id,
			media_body=file_path
		).execute()


if __name__ == '__main__':
	chart_id = 94
	chart = chart_repository.get_chart_by_id(94)
	chart = chart.fill()
	uploader = YTUploader()
	uploader.upload_video(chart)
