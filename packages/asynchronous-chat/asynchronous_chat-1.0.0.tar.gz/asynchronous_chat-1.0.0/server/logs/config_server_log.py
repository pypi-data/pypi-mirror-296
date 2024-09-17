"""Кофнфиг серверного логера"""

import sys
import os
import logging
from logging.handlers import RotatingFileHandler

from common.variables import LOGGING_LEVEL

# создаём формировщик логов (formatter):
SERVER_FORMATTER = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')

# Подготовка имени файла для логирования
PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'server.log')

# создаём регистратор и настраиваем его
LOGGER = logging.getLogger('server')
# Уровень логирования
LOGGER.setLevel(LOGGING_LEVEL)

STREAM_HANDLER = logging.StreamHandler(sys.stderr)
STREAM_HANDLER.setFormatter(SERVER_FORMATTER)
LOGGER.addHandler(STREAM_HANDLER)

# логи по дням
LOG_FILE = logging.handlers.TimedRotatingFileHandler(PATH, encoding='utf8', interval=1, when='D')
LOG_FILE.setFormatter(SERVER_FORMATTER)
LOGGER.addHandler(LOG_FILE)

if __name__ == '__main__':
    LOGGER.critical('Критическая ошибка')
    LOGGER.error('Ошибка')
    LOGGER.debug('Отладочная информация')
    LOGGER.info('Информационное сообщение')
