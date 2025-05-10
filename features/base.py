#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import inspect
import re
from abc import ABCMeta, abstractmethod
from pathlib import Path
from contextlib import contextmanager
import time

import pandas as pd
import numpy as np


@contextmanager
def timer(name):
    t0 = time.time()
    print(f'[{name}] start')
    yield
    print(f'[{name}] done in {time.time() - t0:.0f} s')


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--force', '-f', action='store_true')
    return parser.parse_args()


def get_features(namespace):
    for k, v in namespace.items():
        if inspect.isclass(v) and issubclass(v, Feature) and not inspect.isabstract(v):
            yield v()


def generate_features(namespace, overwrite=False):
    for feature in get_features(namespace):
        if feature.train_path.exists() and feature.test_path.exists() and not overwrite:
            print(f'{feature.name} was skipped')
        else:
            feature.run().save()


class Feature(metaclass=ABCMeta):
    prefix = ''
    suffix = ''
    dir = '.'

    def __init__(self):
        if self.__class__.__name__.isupper():
            self.name = self.__class__.__name__.lower()
        else:
            self.name = re.sub("([A-Z])", lambda x: "_" + x.group(1).lower(), self.__class__.__name__).lstrip('_')

        self.train = pd.DataFrame()
        self.test = pd.DataFrame()
        self.train_path = Path(self.dir) / f'{self.name}_train.ftr'
        self.test_path = Path(self.dir) / f'{self.name}_test.ftr'

    def run(self):
        with timer(self.name):
            self.create_features()
            prefix = self.prefix + '_' if self.prefix else ''
            suffix = '_' + self.suffix if self.suffix else ''
            self.train.columns = prefix + self.train.columns + suffix
            self.test.columns = prefix + self.test.columns + suffix
        return self

    @abstractmethod
    def create_features(self):
        raise NotImplementedError

    def save(self):
        self.train.to_feather(str(self.train_path))
        self.test.to_feather(str(self.test_path))

    def load(self):
        self.train = pd.read_feather(str(self.train_path))
        self.test = pd.read_feather(str(self.test_path))


class TitanicFeatures(Feature):
    def create_features(self):
        # データの読み込み
        train = pd.read_csv('data/input/train.csv')
        test = pd.read_csv('data/input/test.csv')

        # 元データを保存
        train.to_csv('data/output/raw_train.csv', index=False)
        test.to_csv('data/output/raw_test.csv', index=False)
        print('[TitanicFeatures] Saved raw train and test data.')

        # 特徴量の生成
        for df, name in zip([train, test], ['train', 'test']):
            # 性別を数値に変換
            df['Sex'] = df['Sex'].map({'male': 0, 'female': 1})
            print(f'[{name}] Sex: male→0, female→1')

            # 年齢の欠損値を中央値で補完
            df['Age'].fillna(df['Age'].median(), inplace=True)
            print(f'[{name}] Age: fillna with median')

            # 運賃の欠損値を中央値で補完
            df['Fare'].fillna(df['Fare'].median(), inplace=True)
            print(f'[{name}] Fare: fillna with median')

            # 乗船港の欠損値を最頻値で補完
            df['Embarked'].fillna(df['Embarked'].mode()[0], inplace=True)
            df['Embarked'] = df['Embarked'].map({'C': 0, 'Q': 1, 'S': 2})
            print(f'[{name}] Embarked: fillna with mode, map to int')

            # 家族サイズの特徴量
            df['FamilySize'] = df['SibSp'] + df['Parch'] + 1
            print(f'[{name}] FamilySize: SibSp + Parch + 1')

            # 単独旅行者かどうか
            df['IsAlone'] = (df['FamilySize'] == 1).astype(int)
            print(f'[{name}] IsAlone: FamilySize==1→1, else 0')

            # 名前から敬称を抽出
            df['Title'] = df['Name'].str.extract(' ([A-Za-z]+)\.', expand=False)
            df['Title'] = df['Title'].replace(['Lady', 'Countess', 'Capt', 'Col', 'Don', 'Dr', 'Major', 'Rev', 'Sir', 'Jonkheer', 'Dona'], 'Rare')
            df['Title'] = df['Title'].replace('Mlle', 'Miss')
            df['Title'] = df['Title'].replace('Ms', 'Miss')
            df['Title'] = df['Title'].replace('Mme', 'Mrs')
            title_mapping = {"Mr": 1, "Miss": 2, "Mrs": 3, "Master": 4, "Rare": 5}
            df['Title'] = df['Title'].map(title_mapping)
            df['Title'] = df['Title'].fillna(0)
            print(f'[{name}] Title: extract and map')

        # 使用する特徴量＋ID＋Survived
        feature_cols = ['PassengerId', 'Pclass', 'Sex', 'Age', 'Fare', 'Embarked', 'FamilySize', 'IsAlone', 'Title']
        train_cols = feature_cols + ['Survived']
        self.train = train[train_cols]
        self.test = test[feature_cols]

        # 加工後データを保存
        self.train.to_feather('data/output/titanic_features_train.ftr')
        self.test.to_feather('data/output/titanic_features_test.ftr')
        print('[TitanicFeatures] Saved processed features as feather files.')
