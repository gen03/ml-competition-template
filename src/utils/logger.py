#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from pathlib import Path
from datetime import datetime

def setup_logger(name, log_dir='logs'):
    """ロガーの設定"""
    # ログディレクトリの作成
    log_dir = Path(log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)

    # ロガーの作成
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # ファイルハンドラの設定
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = log_dir / f'{name}_{timestamp}.log'
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)

    # コンソールハンドラの設定
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # フォーマッタの設定
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # ハンドラの追加
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger