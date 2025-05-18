#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json
import logging
from pathlib import Path

import pandas as pd
import numpy as np
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score, roc_auc_score

from preprocessing import TitanicPreprocessor
from models.lgbm import LGBMModel
from utils.logger import setup_logger


def preprocess_data(config, force=False):
    """データの前処理を実行"""
    logger = logging.getLogger(__name__)
    logger.info('Preprocessing data...')

    preprocessor = TitanicPreprocessor()
    train, test = preprocessor.preprocess(force=force)

    return train, test


def train_and_evaluate(config, train, test):
    """モデルの学習と評価を実行"""
    logger = logging.getLogger(__name__)

    # データの準備
    X_train = train.drop(['Survived', 'PassengerId'], axis=1)
    y_train = train['Survived']
    X_test = test.drop(['PassengerId'], axis=1)

    # クロスバリデーションの設定
    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = []

    # クロスバリデーション
    logger.info('Starting cross-validation...')
    for fold, (train_idx, val_idx) in enumerate(cv.split(X_train), 1):
        logger.info(f'Training fold {fold}/5')

        # データの分割
        X_tr = X_train.iloc[train_idx]
        y_tr = y_train.iloc[train_idx]
        X_val = X_train.iloc[val_idx]
        y_val = y_train.iloc[val_idx]

        # モデルの学習
        model = LGBMModel(config['model'])
        model.train(X_tr, y_tr, X_val, y_val)

        # 検証データでの予測
        val_preds = model.predict(X_val)
        val_score = accuracy_score(y_val, (val_preds > 0.5).astype(int))
        cv_scores.append(val_score)

        logger.info(f'Fold {fold} validation score: {val_score:.4f}')

    # クロスバリデーションスコアの平均
    mean_cv_score = np.mean(cv_scores)
    logger.info(f'Mean CV score: {mean_cv_score:.4f}')

    # 全データでの学習
    logger.info('Training final model...')
    final_model = LGBMModel(config['model'])
    final_model.train(X_train, y_train)

    # テストデータでの予測
    logger.info('Making predictions...')
    test_preds = final_model.predict(X_test)

    return final_model, test_preds, mean_cv_score


def create_submission(config, test, preds):
    """提出ファイルの作成"""
    logger = logging.getLogger(__name__)
    logger.info('Creating submission file...')

    submission = pd.DataFrame({
        'PassengerId': test['PassengerId'],
        'Survived': (preds > 0.5).astype(int)
    })

    submission.to_csv(config['data']['submission'], index=False)
    logger.info(f'Submission file saved to {config["data"]["submission"]}')


def main():
    # 引数の解析
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, default='configs/default.json')
    parser.add_argument('--force', '-f', action='store_true')
    parser.add_argument('--skip-preprocess', action='store_true', help='前処理をスキップ')
    args = parser.parse_args()

    # ロガーの設定
    logger = setup_logger(__name__)

    # 設定の読み込み
    with open(args.config) as f:
        config = json.load(f)

    # 前処理
    if not args.skip_preprocess:
        train, test = preprocess_data(config, args.force)
    else:
        logger.info('Loading preprocessed data...')
        train = pd.read_feather('data/output/titanic_features_train.ftr')
        test = pd.read_feather('data/output/titanic_features_test.ftr')

    # モデルの学習と評価
    model, test_preds, cv_score = train_and_evaluate(config, train, test)

    # 提出ファイルの作成
    create_submission(config, test, test_preds)

    logger.info('Done!')


if __name__ == '__main__':
    main()
