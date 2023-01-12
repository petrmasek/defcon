import requests
import time
from enum import Enum

class DefconNotifierType(Enum):
	TELEGRAM = 1
	FILE = 2
	SCREEN = 3

class DefconNotifier:
	__OUTTPUT_FILE = 'defcon.data'

	def __init__(self, bot_id: str, group_id: str, type: DefconNotifierType = 1) -> None:
		self.__bot_id = bot_id
		self.__group_id = group_id
		self.__type = type

	def __send_message_to_telegram(self, message: str) -> None:
		url = f'https://api.telegram.org/bot{self.__bot_id}/sendMessage'
		params = {
			'chat_id': self.__group_id,
			'text' : message,
			'parse_mode' : 'markdown'
		}
		_ = requests.get(url, params)

	def __send_message_to_file(self, message: str) -> None:
		with open(DefconNotifier.__OUTTPUT_FILE, "a") as data_file:
			now = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
			data_file.write(f'{now} - {message}\n')

	def __send_message_to_screen(self, message: str) -> None:
		print(message)

	def __send_message(self, message: str) -> None:
		if self.__type == DefconNotifierType.TELEGRAM:
			self.__send_message_to_telegram(message)
		elif self.__type == DefconNotifierType.FILE:
			self.__send_message_to_file(message)
		elif self.__type == DefconNotifierType.SCREEN:
			self.__send_message_to_screen(message)

	def send_event(self, defcon_level: int) -> None:
		message = f'*DEFCON: {defcon_level}*'
		self.__send_message(message)
