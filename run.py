#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json
import logging
from pathlib import Path

import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import KFold

from features.create import generate_features
from models.lgbm import LGBMModel
from utils.logger import setup_logger


def main():
    # 引数の解析
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, default='configs/default.json')
    parser.add_argument('--force', '-f', action='store_true')
    args = parser.parse_args()

    # ロガーの設定
    logger = setup_logger(__name__)

    # 設定の読み込み
    with open(args.config) as f:
        config = json.load(f)

    # 特徴量の生成
    logger.info('Generating features...')
    generate_features(force=args.force)

    # データの読み込み
    logger.info('Loading data...')
    train = pd.read_csv(config['data']['train'])
    test = pd.read_csv(config['data']['test'])

    # モデルの学習
    logger.info('Training model...')
    model = LGBMModel(config['model'])
    model.train(train)

    # 予測
    logger.info('Making predictions...')
    submission = model.predict(test)

    # 提出ファイルの保存
    logger.info('Saving submission...')
    submission.to_csv(config['data']['submission'], index=False)

    logger.info('Done!')


if __name__ == '__main__':
    main()
