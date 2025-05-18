#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from pathlib import Path
import logging
import pyarrow.feather as feather
import lightgbm as lgb
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score
import json
from datetime import datetime

logger = logging.getLogger(__name__)

FEATURE_DIR = Path('data/03_features')
MODEL_DIR = Path('models')
MODEL_DIR.mkdir(parents=True, exist_ok=True)

class ModelTrainer:
    def __init__(self, input_dir='data/03_features', output_dir='models'):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # モデルのパラメータ
        self.params = {
            'objective': 'binary',
            'metric': 'binary_logloss',
            'boosting_type': 'gbdt',
            'num_leaves': 31,
            'learning_rate': 0.05,
            'feature_fraction': 0.9,
            'bagging_fraction': 0.8,
            'bagging_freq': 5,
            'max_depth': 6,
            'min_data_in_leaf': 20,
            'lambda_l1': 0.1,
            'lambda_l2': 0.1
        }

    def train(self, n_splits=5, random_state=42):
        """モデルを学習"""
        # データの読み込み
        train = feather.read_feather(self.input_dir / 'train.ftr')
        test = feather.read_feather(self.input_dir / 'test.ftr')

        # 目的変数と特徴量
        if 'target' in train.columns:
            y = train['target']
            X = train.drop(['target'], axis=1)
        elif 'Survived' in train.columns:
            y = train['Survived']
            X = train.drop(['Survived'], axis=1)
        else:
            raise ValueError('目的変数カラムが見つかりません')

        # 学習・バリデーション分割
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=random_state, stratify=y)

        # LightGBMデータセット
        lgb_train = lgb.Dataset(X_train, y_train)
        lgb_val = lgb.Dataset(X_val, y_val, reference=lgb_train)

        # コールバックの設定
        callbacks = [
            lgb.early_stopping(stopping_rounds=50),
            lgb.log_evaluation(period=100)
        ]

        # モデルの学習
        model = lgb.train(
            self.params,
            lgb_train,
            valid_sets=[lgb_train, lgb_val],
            num_boost_round=1000,
            callbacks=callbacks
        )

        # バリデーション評価
        val_pred = (model.predict(X_val) > 0.5).astype(int)
        acc = accuracy_score(y_val, val_pred)
        auc = roc_auc_score(y_val, model.predict(X_val))
        logger.info(f'Validation Accuracy: {acc:.4f}, AUC: {auc:.4f}')

        # スコアの保存
        self._save_scores([acc, auc])

        # モデルの保存
        model_path = self.output_dir / 'model_lgbm.txt'
        model.save_model(str(model_path))
        logger.info(f'モデルを保存しました: {model_path}')

        return model

    def _save_scores(self, scores):
        """スコアを保存"""
        scores_file = self.output_dir / 'scores.json'

        scores_dict = {
            'scores': scores,
            'mean_score': np.mean(scores),
            'std_score': np.std(scores)
        }

        with open(scores_file, 'w') as f:
            json.dump(scores_dict, f, indent=2)

        logger.info(f'Saved scores to {scores_file}')

if __name__ == '__main__':
    trainer = ModelTrainer()
    trainer.train()