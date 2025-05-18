#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from pathlib import Path
import json
from datetime import datetime
import logging
import pyarrow as pa
import pyarrow.feather as feather

logger = logging.getLogger(__name__)

class TitanicPreprocessor:
    def __init__(self, input_dir='data/input', output_dir='data/output'):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # 前処理の設定
        self.config = {
            'categorical_mappings': {
                'Sex': {'male': 0, 'female': 1},
                'Embarked': {'C': 0, 'Q': 1, 'S': 2},
                'Title': {
                    'Mr': 1, 'Miss': 2, 'Mrs': 3, 'Master': 4, 'Rare': 5
                }
            },
            'rare_titles': [
                'Lady', 'Countess', 'Capt', 'Col', 'Don', 'Dr',
                'Major', 'Rev', 'Sir', 'Jonkheer', 'Dona'
            ],
            'title_replacements': {
                'Mlle': 'Miss',
                'Ms': 'Miss',
                'Mme': 'Mrs'
            }
        }

        # 前処理の統計情報を保存
        self.stats = {
            'train': {},
            'test': {}
        }

    def preprocess(self, force=False):
        """前処理を実行し、結果を保存"""
        # 元データの読み込み
        train = pd.read_csv(self.input_dir / 'train.csv')
        test = pd.read_csv(self.input_dir / 'test.csv')

        # 元データの保存
        train.to_csv(self.output_dir / 'raw_train.csv', index=False)
        test.to_csv(self.output_dir / 'raw_test.csv', index=False)
        logger.info('Saved raw data')

        # 前処理の実行
        train_processed = self._process_data(train, 'train')
        test_processed = self._process_data(test, 'test')

        # 前処理済みデータの保存（Feather形式）
        self._save_feather(train_processed, 'titanic_features_train.ftr')
        self._save_feather(test_processed, 'titanic_features_test.ftr')
        logger.info('Saved processed data')

        # 前処理の統計情報を保存
        self._save_stats()

        return train_processed, test_processed

    def _save_feather(self, df, filename):
        """Feather形式でデータを保存"""
        # データ型の最適化
        df = df.copy()
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].astype('category')

        # Feather形式で保存
        feather.write_feather(df, self.output_dir / filename, compression='lz4')
        logger.info(f'Saved {filename}')

    def _process_data(self, df, dataset_name):
        """データの前処理を実行"""
        df = df.copy()

        # 性別の変換
        df['Sex'] = df['Sex'].map(self.config['categorical_mappings']['Sex'])
        self.stats[dataset_name]['sex_mapping'] = dict(df['Sex'].value_counts())

        # 年齢の欠損値補完
        age_median = df['Age'].median()
        df['Age'] = df['Age'].fillna(age_median)
        self.stats[dataset_name]['age_median'] = age_median
        self.stats[dataset_name]['age_missing'] = df['Age'].isnull().sum()

        # 運賃の欠損値補完
        fare_median = df['Fare'].median()
        df['Fare'] = df['Fare'].fillna(fare_median)
        self.stats[dataset_name]['fare_median'] = fare_median
        self.stats[dataset_name]['fare_missing'] = df['Fare'].isnull().sum()

        # 乗船港の欠損値補完
        embarked_mode = df['Embarked'].mode()[0]
        df['Embarked'] = df['Embarked'].fillna(embarked_mode)
        df['Embarked'] = df['Embarked'].map(self.config['categorical_mappings']['Embarked'])
        self.stats[dataset_name]['embarked_mode'] = embarked_mode
        self.stats[dataset_name]['embarked_missing'] = df['Embarked'].isnull().sum()

        # 家族サイズの特徴量
        df['FamilySize'] = df['SibSp'] + df['Parch'] + 1
        self.stats[dataset_name]['family_size_stats'] = {
            'mean': df['FamilySize'].mean(),
            'std': df['FamilySize'].std(),
            'min': df['FamilySize'].min(),
            'max': df['FamilySize'].max()
        }

        # 単独旅行者かどうか
        df['IsAlone'] = (df['FamilySize'] == 1).astype(int)
        self.stats[dataset_name]['is_alone_ratio'] = df['IsAlone'].mean()

        # 名前から敬称を抽出
        df['Title'] = df['Name'].str.extract(' ([A-Za-z]+)\.', expand=False)
        df['Title'] = df['Title'].replace(self.config['rare_titles'], 'Rare')
        df['Title'] = df['Title'].replace(self.config['title_replacements'])
        df['Title'] = df['Title'].map(self.config['categorical_mappings']['Title'])
        df['Title'] = df['Title'].fillna(0)
        self.stats[dataset_name]['title_distribution'] = dict(df['Title'].value_counts())

        # 必要なカラムのみを残す
        keep_cols = ['PassengerId', 'Pclass', 'Sex', 'Age', 'Fare', 'Embarked', 'FamilySize', 'IsAlone', 'Title']
        if 'Survived' in df.columns:
            keep_cols.append('Survived')
        df = df[keep_cols]
        return df

    def _convert_to_serializable(self, obj):
        """numpyの数値型をPythonの標準型に変換"""
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {k: self._convert_to_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_to_serializable(item) for item in obj]
        return obj

    def _save_stats(self):
        """前処理の統計情報を保存"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        stats_file = self.output_dir / f'preprocessing_stats_{timestamp}.json'

        # numpyの数値型をPythonの標準型に変換
        serializable_stats = self._convert_to_serializable(self.stats)

        with open(stats_file, 'w') as f:
            json.dump(serializable_stats, f, indent=2)

        logger.info(f'Saved preprocessing statistics to {stats_file}')