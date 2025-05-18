#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class DataPreprocessor:
    def __init__(self, input_dir='data/01_raw', output_dir='data/02_processed'):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def make_dataset(self):
        """データセットの前処理"""
        # データの読み込み
        train = pd.read_csv(self.input_dir / 'train.csv')
        test = pd.read_csv(self.input_dir / 'test.csv')

        # train/test結合
        train['is_train'] = 1
        test['is_train'] = 0
        all_data = pd.concat([train, test], sort=False, ignore_index=True)

        # 一括前処理
        all_data = self._preprocess_data(all_data)

        # train/test分割
        train_processed = all_data[all_data['is_train'] == 1].drop(['is_train'], axis=1)
        test_processed = all_data[all_data['is_train'] == 0].drop(['is_train'], axis=1)

        # 保存
        train_processed.to_csv(self.output_dir / 'train.csv', index=False)
        test_processed.to_csv(self.output_dir / 'test.csv', index=False)
        logger.info(f'Saved processed data to {self.output_dir}')

    def _preprocess_data(self, df):
        """データの前処理"""
        # 年齢の欠損値を中央値で補完
        df['Age'] = df['Age'].fillna(df['Age'].median())

        # 運賃の欠損値を中央値で補完
        df['Fare'] = df['Fare'].fillna(df['Fare'].median())

        # 乗船港の欠損値を最頻値で補完
        df['Embarked'] = df['Embarked'].fillna(df['Embarked'].mode()[0])

        # 客室番号の欠損値を'U'で補完
        df['Cabin'] = df['Cabin'].fillna('U')

        # 客室番号の最初の文字を抽出
        df['Cabin'] = df['Cabin'].str[0]

        return df

if __name__ == '__main__':
    preprocessor = DataPreprocessor()
    preprocessor.make_dataset()