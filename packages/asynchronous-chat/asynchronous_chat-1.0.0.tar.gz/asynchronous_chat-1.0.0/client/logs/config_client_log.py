"""Конфиг клиентского логера"""

import sys
import os
import logging

from common.variables import LOGGING_LEVEL

# создаём формировщик логов (formatter):
CLIENT_FORMATTER = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')

# Подготовка имени файла для логирования
PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'client.log')

# создаём регистратор и настраиваем его
LOGGER = logging.getLogger('client')
# Уровень логирования
LOGGER.setLevel(LOGGING_LEVEL)

# создаём потоки вывода логов
# вывод в консоль
STREAM_HANDLER = logging.StreamHandler(sys.stderr)
STREAM_HANDLER.setFormatter(CLIENT_FORMATTER)
LOGGER.addHandler(STREAM_HANDLER)

# сохранение в файл
LOG_FILE = logging.FileHandler(PATH, encoding='utf8')
LOG_FILE.setFormatter(CLIENT_FORMATTER)
LOGGER.addHandler(LOG_FILE)

if __name__ == '__main__':
    LOGGER.critical('Критическая ошибка')
    LOGGER.error('Ошибка')
    LOGGER.debug('Отладочная информация')
    LOGGER.info('Информационное сообщение')
