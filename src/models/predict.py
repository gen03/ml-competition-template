#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from pathlib import Path
import logging
import pyarrow.feather as feather
import lightgbm as lgb

logger = logging.getLogger(__name__)

class Predictor:
    def __init__(self, input_dir='data/03_features', output_dir='data/04_submission'):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def predict(self):
        """予測を実行"""
        # データの読み込み
        test = feather.read_feather(self.input_dir / 'test.ftr')

        # モデルの読み込み
        model = lgb.Booster(model_file='models/model_lgbm.txt')

        # 学習データと同じ特徴量のみを使用
        feature_names = model.feature_name()
        test_features = test[feature_names]

        # 予測
        pred = model.predict(test_features)
        pred = (pred > 0.5).astype(int)

        # 提出用データの作成
        submission = pd.DataFrame({
            'PassengerId': test['PassengerId'],
            'Survived': pred
        })

        # 保存（上書き）
        submission_path = self.output_dir / 'submission.csv'
        submission.to_csv(submission_path, index=False, mode='w')
        logger.info(f'予測結果を上書き保存しました: {submission_path}')

if __name__ == '__main__':
    predictor = Predictor()
    predictor.predict()