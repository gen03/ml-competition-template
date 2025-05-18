#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from pathlib import Path
import logging
import pyarrow.feather as feather

logger = logging.getLogger(__name__)

class FeatureBuilder:
    def __init__(self, input_dir='data/02_processed', output_dir='data/03_features'):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def build_features(self):
        """特徴量を生成"""
        # データの読み込み
        train = pd.read_csv(self.input_dir / 'train.csv')
        test = pd.read_csv(self.input_dir / 'test.csv')

        # train/test結合
        train['is_train'] = 1
        test['is_train'] = 0
        all_data = pd.concat([train, test], sort=False, ignore_index=True)

        # 基本的な特徴量の作成
        all_data = self._create_basic_features(all_data)

        # カテゴリカル変数のダミー変数化
        categorical_cols = ['Sex', 'Embarked', 'Age_bin', 'Fare_bin', 'FamilySize_bin']
        all_data = pd.get_dummies(all_data, columns=categorical_cols, drop_first=False)

        # Embarkedカラムの形式を統一（浮動小数点形式に変換）
        embarked_cols = [col for col in all_data.columns if col.startswith('Embarked_')]
        for col in embarked_cols:
            all_data[col] = all_data[col].astype(float)

        # train/testに分割
        train_features = all_data[all_data['is_train'] == 1].drop(['is_train'], axis=1).reset_index(drop=True)
        test_features = all_data[all_data['is_train'] == 0].drop(['is_train'], axis=1).reset_index(drop=True)

        # 特徴量の保存
        self._save_features(train_features, test_features)

    def _create_basic_features(self, df):
        """基本的な特徴量を作成"""
        # 必要なカラムのみ選択
        keep_cols = ['PassengerId', 'Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked', 'is_train']
        if 'Survived' in df.columns:
            keep_cols.append('Survived')
        df = df[keep_cols].copy()  # コピーを作成して警告を解消

        # 年齢の欠損値を中央値で補完
        df.loc[:, 'Age'] = df['Age'].fillna(df['Age'].median())

        # 年齢のビン分割（重複を許容）
        df.loc[:, 'Age_bin'] = pd.qcut(df['Age'], q=5, labels=False, duplicates='drop')

        # 運賃の欠損値を中央値で補完
        df.loc[:, 'Fare'] = df['Fare'].fillna(df['Fare'].median())

        # 運賃のビン分割
        df.loc[:, 'Fare_bin'] = pd.qcut(df['Fare'], q=5, labels=False)

        # 家族サイズ
        df.loc[:, 'FamilySize'] = df['SibSp'] + df['Parch'] + 1

        # 家族サイズのビン分割
        df.loc[:, 'FamilySize_bin'] = pd.cut(df['FamilySize'],
                                    bins=[0, 1, 4, 11],
                                    labels=[0, 1, 2])

        return df

    def _save_features(self, train_features, test_features):
        """特徴量を保存"""
        # Feather形式で保存
        feather.write_feather(train_features, self.output_dir / 'train.ftr')
        feather.write_feather(test_features, self.output_dir / 'test.ftr')
        logger.info(f'Saved features to {self.output_dir}')

if __name__ == '__main__':
    feature_builder = FeatureBuilder()
    feature_builder.build_features()