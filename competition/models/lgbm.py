#!/usr/bin/env python
# -*- coding: utf-8 -*-

import lightgbm as lgb
import numpy as np
import pandas as pd
from sklearn.model_selection import KFold


class LGBMModel:
    def __init__(self, params):
        self.params = params
        self.models = []

    def train(self, X, y, X_val=None, y_val=None):
        # バリデーションデータが与えられている場合
        if X_val is not None and y_val is not None:
            train_set = lgb.Dataset(X, y)
            valid_set = lgb.Dataset(X_val, y_val, reference=train_set)
            model = lgb.train(
                params=self.params['params'],
                train_set=train_set,
                valid_sets=[train_set, valid_set],
                num_boost_round=1000,
                callbacks=[lgb.log_evaluation(period=100)]
            )
            self.models.append(model)
        else:
            # 全データで学習
            train_set = lgb.Dataset(X, y)
            model = lgb.train(
                params=self.params['params'],
                train_set=train_set,
                num_boost_round=1000,
                callbacks=[lgb.log_evaluation(period=100)]
            )
            self.models.append(model)

    def predict(self, X):
        # 予測（確率値を返す）
        preds = []
        for model in self.models:
            pred = model.predict(X)
            preds.append(pred)
        pred = np.mean(preds, axis=0)
        return pred
