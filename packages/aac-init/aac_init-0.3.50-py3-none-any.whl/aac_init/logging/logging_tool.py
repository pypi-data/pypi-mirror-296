# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Rudy Lei <shlei@cisco.com>

import os
from loguru import logger
from aac_init.conf import settings


def setup_logger(log_file):
    """
    Setup logger with log rotation.

    :param log_file: log file name
    """
    log_file_path = os.path.join(settings.OUTPUT_BASE_DIR, "aac_init_log", log_file)

    logger.add(
        sink=log_file_path,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        encoding="utf-8",
        rotation="5 MB",
    )

    return logger


def netmiko_session_logger(log_file):
    """
    Setup netmiko session_log path.

    :param log_file: log file name
    """
    log_file_path = os.path.join(settings.OUTPUT_BASE_DIR, "aac_init_log", log_file)

    return log_file_path
