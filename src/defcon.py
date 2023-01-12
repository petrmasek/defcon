import daemon
import daemon.pidfile
import os
import signal
import sys
import time

from defconlogger import DefconLogger
from defconconfig import DefconConfig
from defconnotifier import DefconNotifier
from defconnotifier import DefconNotifierType
from defcondownloader import DefconDownloader

class DefconApp:
	__DEFCON_DATA_DIR = 'data'
	__DEFCON_PID_FILE_NAME = 'defcon.pid'
	__DEFCON_LEVEL_FILE_NAME = 'defcon.level'

	__DEFAULT_DEFCON_LEVEL = 0

	def __init__(self) -> None:
		self.__logger = DefconLogger.getLogger()
		self.__config = DefconConfig()
		self.__is_daemon = False
		if not os.path.isdir(DefconApp.__DEFCON_DATA_DIR):
			os.mkdir(DefconApp.__DEFCON_DATA_DIR)
		self.__working_directory = os.getcwd()
		self.__pidfile = daemon.pidfile.PIDLockFile(f'{self.__working_directory}/{DefconApp.__DEFCON_DATA_DIR}/{DefconApp.__DEFCON_PID_FILE_NAME}')
		self.__running = True
		self.__defcon_level = DefconApp.__DEFAULT_DEFCON_LEVEL

	def __get_defcon_level_file_path(self) -> str:
		return f'{DefconApp.__DEFCON_DATA_DIR}/{DefconApp.__DEFCON_LEVEL_FILE_NAME}'

	def __load_defcon_level(self) -> int:
		result = self.__defcon_level
		if os.path.isfile(self.__get_defcon_level_file_path()):
			with open(self.__get_defcon_level_file_path(), "r") as level_file:
				try:
					result = int(level_file.read())
					self.__logger.info(f'Program has loaded last saved defcon level: {result}')
				except ValueError:
					self.__logger.error(f'Program can not read the defcon level file: {self.__get_defcon_level_file_path()}')
		return result
	
	def __save_defcon_level(self) -> None:
		if not os.path.isdir(DefconApp.__DEFCON_DATA_DIR):
			os.mkdir(DefconApp.__DEFCON_DATA_DIR)
		try:
			with open(self.__get_defcon_level_file_path(), "w") as level_file:
				level_file.write(f'{self.__defcon_level}')
				self.__logger.info(f'Program has saved new defcon level: {self.__defcon_level}')
		except PermissionError:
			self.__logger.error(f'Program can not write to the defcon level file: {self.__get_defcon_level_file_path()}')
	
	def __get_notification_type(self) -> DefconNotifierType:
		if self.__config.is_debug():
			if self.__is_daemon:
				return DefconNotifierType.FILE
			return DefconNotifierType.SCREEN
		return DefconNotifierType.TELEGRAM

	def run(self) -> None:
		self.__logger.info('Program has started watching Defcon warning system')
		self.__defcon_level = self.__load_defcon_level()
		notifier = DefconNotifier(self.__config.get_telegram_bot_id(), self.__config.get_telegram_trading_group_id(), self.__get_notification_type())
		while self.__running:
			try:
				downloader = DefconDownloader()
				defcon_level = downloader.download()
				if defcon_level != self.__defcon_level:
					self.__defcon_level = defcon_level
					notifier.send_event(defcon_level)
					self.__save_defcon_level()
				time.sleep(self.__config.get_defcon_check_period())
			except KeyboardInterrupt:
				self.__running = False
				self.__logger.info('Program has been stopped manually!')

	def start(self) -> None:
		with daemon.DaemonContext(working_directory = self.__working_directory, pidfile = self.__pidfile, files_preserve = [ handler.stream.fileno() for handler in self.__logger.handlers ]):
			self.__is_daemon = True
			self.__logger.info('Program is a daemon')
			self.run()

	def stop(self) -> None:
		pid = self.__pidfile.read_pid()
		if pid != None:
			self.__is_daemon = False
			os.kill(pid, signal.SIGTERM)
			self.__logger.info('Program has been stopped')

	def restart(self) -> None:
		self.stop()
		self.start()

def main():
	if len(sys.argv) > 1:
		cmd = sys.argv[1]
		if cmd == 'start':
			DefconApp().start()
		elif cmd == 'stop':
			DefconApp().stop()
		elif cmd == 'restart':
			DefconApp().restart()
		else:
			print(f'Usage {sys.argv[0]} start|stop|restart')
	else:
		print(f'if you want to use this tool as daemon, use: {sys.argv[0]} start|stop|restart')
		DefconApp().run()
	sys.exit(0)

if __name__ == "__main__":
    main()