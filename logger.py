# -*- coding: utf-8 -*-

#   2019/5/27 0027 上午 11:48     

__author__ = 'RollingBear'

import logging
import logging.handlers

import os
import sys

LEVELS = {'NOTSET': logging.NOTSET,
          'DEBUG': logging.DEBUG,
          'INFO': logging.INFO,
          'WARNING': logging.WARNING,
          'ERROR': logging.ERROR,
          'CRITICAL': logging.CRITICAL}


def config_logging(file_name='log.log', log_level='NOTSET'):
    logs_dir = os.path.join(os.path.dirname(__file__), 'logs')

    if os.path.exists(logs_dir) and os.path.isdir(logs_dir):
        pass

    else:
        os.makedirs(logs_dir)

    logging.getLogger('').handlers = []

    file_name = os.path.join(logs_dir, file_name)

    rotatingFileHandler = logging.handlers.RotatingFileHandler(filename=file_name, maxBytes=1024 * 1024 * 50,
                                                               backupCount=5)
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    rotatingFileHandler.setFormatter(formatter)

    logging.getLogger('').addHandler(rotatingFileHandler)

    console = logging.StreamHandler()
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)

    logging.getLogger('').addHandler(console)

    logger = logging.getLogger('')
    level = LEVELS[log_level.upper()]
    logger.setLevel(level)


def config_logging_plus(file_name='log.log', log_level='NOTSET', remote_address=('127.0.0.1', 8888),
                        write_console=False):
    logs_dir = os.path.join(os.path.dirname(__file__), 'logs')

    if os.path.exists(logs_dir) and os.path.isdir(logs_dir):
        pass

    else:
        os.makedirs(logs_dir)

    if file_name is None:
        file_name = os.path.splitext(sys.argv[0])[0]
        file_name = os.path.join(logs_dir, '%s_%s.log' % (file_name, os.getpid()))
    else:
        file_name = os.path.join(logs_dir, file_name)

    logging.getLogger('').handlers = []

    rotatingFileHandler = logging.handlers.RotatingFileHandler(filename=file_name, maxBytes=1024 * 1024 * 50,
                                                               backupCount=5)
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    rotatingFileHandler.setFormatter(formatter)

    logging.getLogger('').addHandler(rotatingFileHandler)

    if write_console is not None and write_console is True:
        console = logging.StreamHandler()

    console.setLevel(logging.NOTSET)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)

    logging.getLogger('').addHandler(console)

    if remote_address is not None and hasattr(remote_address, '__iter__') and len(remote_address) > 1:
        socketHandler = logging.handlers.SocketHandler(remote_address[0], remote_address[1])

    formatter = logging.Formatter('%(asctime)s %(processName)s %(process)s %(name)-12s %(levelname)-8s %(message)s')
    socketHandler.setFormatter(formatter)

    logging.getLogger('').addHandler(socketHandler)

    logger = logging.getLogger('')
    level = LEVELS[log_level.upper()]
    logger.setLevel(level)
