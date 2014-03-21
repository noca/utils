#!/usr/bin/env python

import os
import logging


from config import log_dir
from config import log_file


def get_logger():
    '''
    @summary: init logger
    @result: return a logger object
    '''
    logger_ = logging.getLogger("employee_account")
    formatter = logging.Formatter
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)-8s] %(message)s', '%Y-%m-%d %H:%M:%S',)
    handler = logging.FileHandler(log_dir + "/" + log_file)
    handler.setFormatter(formatter)
    logger_.addHandler(handler)
    logger_.setLevel(logging.DEBUG)
    return logger_

if not os.path.isdir(log_dir):
    os.makedirs(log_dir)

logger = get_logger()
