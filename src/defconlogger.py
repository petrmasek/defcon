import logging.config
import os

class DefconLogger:
	__LOGS_DIR = 'logs'
	__LOGGING_CONFIG_FILE = 'config/logging.config'

	@staticmethod
	def getLogger() -> logging.Logger:
		if not os.path.isdir(DefconLogger.__LOGS_DIR):
			os.mkdir(DefconLogger.__LOGS_DIR)
		logging.config.fileConfig(fname = DefconLogger.__LOGGING_CONFIG_FILE, disable_existing_loggers = False)
		return logging.getLogger()
