#!/usr/bin/env python
# -*- coding: utf-8 -*-

# %%
"""
Titanicデータセットの探索的分析（EDA）
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# %%
# 表示設定
plt.style.use('seaborn')
sns.set(font_scale=1.2)
plt.rcParams['figure.figsize'] = [10, 6]
plt.rcParams['font.family'] = 'sans-serif'

# プロジェクトのルートディレクトリを取得
ROOT_DIR = Path(__file__).parent.parent

# %%
def load_data():
    """データの読み込み"""
    train = pd.read_csv(ROOT_DIR / 'data/01_raw/train.csv')
    test = pd.read_csv(ROOT_DIR / 'data/01_raw/test.csv')
    return train, test

# %%
def check_basic_info(train, test):
    """基本情報の確認"""
    print('\n=== Train Info ===')
    print(train.info())
    print('\n=== Test Info ===')
    print(test.info())

    print('\n=== Train Statistics ===')
    print(train.describe())
    print('\n=== Test Statistics ===')
    print(test.describe())

# %%
def check_missing_values(train, test):
    """欠損値の確認"""
    print('\n=== Train Missing Values ===')
    print(train.isnull().sum())
    print('\n=== Test Missing Values ===')
    print(test.isnull().sum())

# %%
def analyze_target(train):
    """目的変数の分析"""
    # 生存率の確認
    survival_rate = train['Survived'].mean()
    print(f'生存率: {survival_rate:.2%}')

    # 可視化
    plt.figure(figsize=(8, 6))
    sns.countplot(x='Survived', data=train)
    plt.title('生存者数')
    plt.savefig(ROOT_DIR / 'notebooks/figures/survival_count.png')
    plt.close()

# %%
def analyze_features(train):
    """特徴量の分析"""
    # 性別と生存率
    plt.figure(figsize=(8, 6))
    sns.barplot(x='Sex', y='Survived', data=train)
    plt.title('性別と生存率')
    plt.savefig(ROOT_DIR / 'notebooks/figures/sex_survival.png')
    plt.close()

    # チケットクラスと生存率
    plt.figure(figsize=(8, 6))
    sns.barplot(x='Pclass', y='Survived', data=train)
    plt.title('チケットクラスと生存率')
    plt.savefig(ROOT_DIR / 'notebooks/figures/class_survival.png')
    plt.close()

    # 年齢と生存率
    plt.figure(figsize=(10, 6))
    sns.histplot(data=train, x='Age', hue='Survived', multiple='stack')
    plt.title('年齢と生存率')
    plt.savefig(ROOT_DIR / 'notebooks/figures/age_survival.png')
    plt.close()

    # 運賃と生存率
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='Survived', y='Fare', data=train)
    plt.title('運賃と生存率')
    plt.savefig(ROOT_DIR / 'notebooks/figures/fare_survival.png')
    plt.close()

# %%
def analyze_correlations(train):
    """特徴量間の関係"""
    # 相関行列
    numeric_cols = ['Survived', 'Pclass', 'Age', 'SibSp', 'Parch', 'Fare']
    corr = train[numeric_cols].corr()

    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm')
    plt.title('相関行列')
    plt.savefig(ROOT_DIR / 'notebooks/figures/correlation_matrix.png')
    plt.close()

    # 性別とチケットクラス
    plt.figure(figsize=(10, 6))
    sns.countplot(x='Pclass', hue='Sex', data=train)
    plt.title('性別とチケットクラス')
    plt.savefig(ROOT_DIR / 'notebooks/figures/sex_class.png')
    plt.close()

# %%
def analyze_family_size(train):
    """家族サイズの分析"""
    # 家族サイズの計算
    train['FamilySize'] = train['SibSp'] + train['Parch'] + 1

    # 家族サイズと生存率
    plt.figure(figsize=(10, 6))
    sns.barplot(x='FamilySize', y='Survived', data=train)
    plt.title('家族サイズと生存率')
    plt.savefig(ROOT_DIR / 'notebooks/figures/family_size_survival.png')
    plt.close()

# %%
def main():
    """メイン関数"""
    # 出力ディレクトリの作成
    os.makedirs(ROOT_DIR / 'notebooks/figures', exist_ok=True)

    # データの読み込み
    train, test = load_data()
    print('Train shape:', train.shape)
    print('Test shape:', test.shape)

    # 基本情報の確認
    check_basic_info(train, test)

    # 欠損値の確認
    check_missing_values(train, test)

    # 目的変数の分析
    analyze_target(train)

    # 特徴量の分析
    analyze_features(train)

    # 特徴量間の関係
    analyze_correlations(train)

    # 家族サイズの分析
    analyze_family_size(train)

    print('\n=== 主な発見 ===')
    print('1. 性別が生存率に大きく影響')
    print('2. チケットクラスが生存率に影響')
    print('3. 年齢と運賃も生存率に関連')
    print('4. 家族サイズも重要な特徴量')

    print('\n=== 次のステップ ===')
    print('1. 欠損値の補完方法の検討')
    print('2. 特徴量エンジニアリングの検討')
    print('3. モデルの選択と学習')

# %%
if __name__ == '__main__':
    main()