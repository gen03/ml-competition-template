#!/bin/bash

# Kaggleの認証情報ディレクトリを作成
mkdir -p ~/.kaggle

# 環境変数から認証情報を取得して設定
echo "{\"username\":\"$KAGGLE_USERNAME\",\"key\":\"$KAGGLE_KEY\"}" > ~/.kaggle/kaggle.json

# 権限を設定
chmod 600 ~/.kaggle/kaggle.json