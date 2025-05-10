#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys
from pathlib import Path


def setup_logger(name, log_level=logging.INFO):
    """ロガーの設定を行う関数

    Args:
        name (str): ロガーの名前
        log_level (int, optional): ログレベル. Defaults to logging.INFO.

    Returns:
        logging.Logger: 設定済みのロガー
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # ハンドラの設定
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger