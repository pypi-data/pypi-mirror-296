import datetime


class Logger:
    def __init__(self, log_file='log/logs/logs.txt'):
        self.log_file = log_file

    def _write_log(self, level, message):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"{timestamp} [{level}] {message}\n"

        with open(self.log_file, 'a') as file:
            file.write(log_message)

    def Error(self, message):
        self._write_log('ERROR', message)

    def Info(self, message):
        self._write_log('INFO', message)

    def Debug(self, message):
        self._write_log('DEBUG', message)
