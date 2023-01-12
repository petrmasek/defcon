import json
from defconlogger import DefconLogger

class DefconConfig:
	__CONFIG_FILE = 'config/defcon.config'
	
	__DEFAULT_DEFCON_CHECK_PERIOD = 60 # seconds

	def __init__(self) -> None:
		self.__logger = DefconLogger.getLogger()

		try:
			with open(DefconConfig.__CONFIG_FILE, 'r') as config_file:
				self.__config = json.load(config_file)
				self.__logger.info('Program has loaded config')
		except Exception as e:
			self.__config = None
			self.__logger.error(f'Program has failed to load config: {e}')

	def get_defcon_check_period(self) -> int:
		if self.__config != None and 'defcon_check_period' in self.__config:
			value = self.__config['defcon_check_period']
			if isinstance(value, int):
				return value
			try:
				return int(value)
			except ValueError:
				return DefconConfig.__DEFAULT_DEFCON_CHECK_PERIOD
		return DefconConfig.__DEFAULT_DEFCON_CHECK_PERIOD

	def get_telegram_bot_id(self) -> str:
		if self.__config != None and 'telegram_bot_id' in self.__config:
			return self.__config['telegram_bot_id']
		return ''

	def get_telegram_trading_group_id(self) -> str:
		if self.__config != None and 'telegram_trading_group_id' in self.__config:
			return self.__config['telegram_trading_group_id']
		return ''

	def is_debug(self) -> bool:
		return self.__config != None and 'debug' in self.__config and self.__config['debug']
