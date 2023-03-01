import logging
import inspect

class Logger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s %(levelname)s %(module)s: %(message)s')

        file_handler = logging.FileHandler('logfile.log')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def _get_info(self):
        frame, filename, line_number, function_name, lines, index = inspect.getouterframes(inspect.currentframe())[2]
        module_name = inspect.getmodule(frame).__name__
        return filename, line_number, module_name

    def debug(self, message):
        filename, line_number, module_name = self._get_info()
        self.logger.debug(f"{filename}:{line_number}  {message}")

    def info(self, message):
        filename, line_number, module_name = self._get_info()
        self.logger.info(f"{filename}:{line_number}  {message}")

    def warning(self, message):
        filename, line_number, module_name = self._get_info()
        self.logger.warning(f"{filename}:{line_number}  {message}")

    def error(self, message):
        filename, line_number, module_name = self._get_info()
        self.logger.error(f"{filename}:{line_number}  {message}")

    def critical(self, message):
        filename, line_number, module_name = self._get_info()
        self.logger.critical(f"{filename}:{line_number}  {message}")
