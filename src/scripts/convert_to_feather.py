#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from pathlib import Path

import pandas as pd


def convert_to_feather():
    # データディレクトリの設定
    data_dir = Path('data/input')

    # 訓練データの変換
    train = pd.read_csv(data_dir / 'train.csv')
    train.to_feather(data_dir / 'train.ftr')

    # テストデータの変換
    test = pd.read_csv(data_dir / 'test.csv')
    test.to_feather(data_dir / 'test.ftr')

    # サンプル提出ファイルの変換
    sample_submission = pd.read_csv(data_dir / 'sample_submission.csv')
    sample_submission.to_feather(data_dir / 'sample_submission.ftr')


if __name__ == '__main__':
    convert_to_feather()
