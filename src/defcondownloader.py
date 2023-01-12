import requests
from datetime import datetime

class DefconDownloader:
	__DEFCON_WARNING_URL = 'https://defconwarningsystem.com/code.dat'

	def __init__(self) -> None:
		self.__last_download = None
		self.__last_level = 0

	def get_last_downloaded_datetime(self) -> datetime:
		return self.__last_download

	def get_last_level(self) -> int:
		return self.__last_level

	def download(self) -> int:
		response = requests.get(DefconDownloader.__DEFCON_WARNING_URL)
		try:
			self.__last_level = int(response.text)
		except ValueError:
			pass
		return self.__last_level
