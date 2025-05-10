# Titanic ML Competition Template

このプロジェクトは、KaggleのTitanicコンペティション用のテンプレートです。機械学習の実験を効率的に行うための構造化された環境を提供します。

## プロジェクト構造

```
.
├── configs/                 # 設定ファイル
│   └── default.json        # デフォルトの設定
├── data/                   # データディレクトリ
│   ├── input/             # 入力データ
│   └── output/            # 出力データ
├── features/              # 特徴量エンジニアリング
├── models/               # モデル定義
├── notebooks/           # Jupyter notebooks
├── utils/              # ユーティリティ関数
├── preprocessing.py    # 前処理スクリプト
├── run.py             # メイン実行スクリプト
└── requirements.txt   # 依存パッケージ
```

## 主要コンポーネント

### 1. 前処理 (`preprocessing.py`)
- データのクリーニング
- 特徴量の生成
- 欠損値の補完
- カテゴリカル変数の変換
- 前処理の統計情報の保存

### 2. モデル学習と評価 (`run.py`)
- クロスバリデーション
- モデルの学習
- 性能評価
- 予測の生成

### 3. 設定 (`configs/default.json`)
- モデルのパラメータ
- データのパス
- その他の設定

## 使用方法

### 1. 環境のセットアップ
```bash
# 依存パッケージのインストール
pip install -r requirements.txt
```

### 2. データの準備
- `data/input/`ディレクトリに以下のファイルを配置：
  - `train.csv`
  - `test.csv`

### 3. 実行方法

#### 通常の実行（前処理から）
```bash
python run.py
```

#### 前処理をスキップして実行
```bash
python run.py --skip-preprocess
```

#### 強制的に前処理を再実行
```bash
python run.py -f
```

#### 設定ファイルを指定して実行
```bash
python run.py --config configs/custom.json
```

### 4. 出力ファイル
- `data/output/raw_train.csv`, `raw_test.csv`: 元データ
- `data/output/titanic_features_train.ftr`, `titanic_features_test.ftr`: 前処理済みデータ
- `data/output/preprocessing_stats_YYYYMMDD_HHMMSS.json`: 前処理の統計情報
- `data/output/submission.csv`: 提出ファイル

## 開発フロー

1. **前処理の実験**
   - `preprocessing.py`を修正
   - 前処理の統計情報を確認
   - 特徴量の追加・修正

2. **モデルの実験**
   - `configs/default.json`でパラメータを調整
   - クロスバリデーションスコアを確認
   - モデルの改善

3. **結果の分析**
   - 前処理の統計情報を分析
   - クロスバリデーションスコアを分析
   - 特徴量の重要度を確認

## 注意事項

- 前処理済みデータは`data/output/`に保存されます
- 統計情報はタイムスタンプ付きで保存されます
- クロスバリデーションは5分割で実行されます
- デフォルトの設定は`configs/default.json`にあります