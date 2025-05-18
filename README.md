# ML Competition Template

## プロジェクト構造
```
.
├── .devcontainer/             # 開発環境設定
│   ├── devcontainer.json     # コンテナ設定
│   └── Dockerfile           # イメージ定義
├── .cursor/                    # Cursor設定
│   └── rules/                 # 開発ルール
│       ├── global-rules.mdc   # 全体ルール
│       └── dev-rules/         # 領域別ルール
├── competition/               # コンペティション関連
│   ├── data/                 # データ
│   │   ├── input/           # 入力データ
│   │   ├── processed/       # 前処理済みデータ
│   │   └── output/          # 出力データ
│   ├── notebooks/           # Jupyter Notebooks
│   │   ├── 01_eda/         # 探索的分析
│   │   ├── 02_feature/     # 特徴量開発
│   │   └── 03_model/       # モデル開発
│   ├── features/            # 特徴量
│   │   ├── base/           # 基本特徴量
│   │   ├── derived/        # 派生特徴量
│   │   └── selection/      # 特徴量選択
│   ├── models/              # 学習済みモデル
│   │   ├── single/         # 単一モデル
│   │   ├── ensemble/       # アンサンブル
│   │   └── submission/     # 提出用モデル
│   └── configs/              # 設定ファイル
│       ├── model.yaml       # モデル設定
│       ├── data.yaml        # データ設定
│       ├── experiment.yaml  # 実験設定
│       └── wandb.json       # W&B設定
├── src/                      # ソースコード
│   ├── data/                # データ処理
│   │   ├── loader.py       # データ読み込み
│   │   └── preprocessor.py # 前処理
│   ├── feature/             # 特徴量生成
│   │   ├── base.py         # 基本特徴量
│   │   └── derived.py      # 派生特徴量
│   ├── model/               # モデル
│   │   ├── base.py         # 基本モデル
│   │   └── ensemble.py     # アンサンブル
│   ├── utils/               # ユーティリティ
│   │   ├── metric.py       # 評価指標
│   │   └── logger.py       # ロギング
│   └── scripts/             # 実行スクリプト
│       ├── train.py        # 学習
│       ├── predict.py      # 予測
│       └── submit.py       # 提出
├── wandb/                    # Weights & Biases
├── tests/                    # テスト
│   ├── data/               # データテスト
│   ├── feature/            # 特徴量テスト
│   └── model/              # モデルテスト
├── .env.example             # 環境変数サンプル
├── .gitignore               # Git除外設定
├── .jupytext.toml           # Jupytext設定
├── docker-compose.yml       # コンテナ設定
├── requirements.txt         # 依存関係
└── README.md                # プロジェクト説明
```

## 開発ワークフロー

### 1. 環境構築と初期設定
- `.devcontainer/`の設定
  - 開発環境の構築
  - 必要なライブラリのインストール
  - 環境変数の設定
- `.cursor/rules/`の設定
  - 開発ルールの確認
  - コーディング規約の設定
  - 実験管理ルールの設定
- `requirements.txt`の準備
  - 必要なパッケージの選定
  - バージョンの固定
  - 依存関係の管理

### 2. データの準備と分析
- `competition/data/input/`の確認
  - データの取得
  - データ形式の確認
  - データの検証
- `competition/notebooks/01_eda/`での分析
  - 基本的な統計量の確認
  - 欠損値の分析
  - 分布の可視化
  - 相関関係の分析
- `competition/data/processed/`の作成
  - 前処理済みデータの保存
  - 中間データの管理
  - データのバージョン管理

### 3. 特徴量エンジニアリング
- `competition/features/base/`の作成
  - 基本的な特徴量の実装
  - カテゴリカル変数の処理
  - 数値変数の変換
- `competition/features/derived/`の開発
  - 派生特徴量の作成
  - 特徴量の組み合わせ
  - ドメイン知識の活用
- `competition/features/selection/`の実装
  - 特徴量の重要度分析
  - 特徴量の選択
  - 次元削減の検討

### 4. モデル開発
- `competition/configs/model/`の設定
  - モデルのパラメータ設定
  - 学習設定の管理
  - 実験設定の記録
- `competition/notebooks/03_model/`での実験
  - モデルの実装
  - 学習と評価
  - 結果の分析
- `competition/models/single/`の管理
  - 単一モデルの保存
  - モデルのバージョン管理
  - 実験結果の記録

### 5. アンサンブルと最適化
- `competition/models/ensemble/`の開発
  - アンサンブルモデルの実装
  - スタッキング/ブレンディング
  - 重みの最適化
- `src/scripts/train.py`の改善
  - 学習プロセスの最適化
  - ハイパーパラメータの調整
  - 学習の効率化
- `src/utils/metric.py`の拡張
  - 評価指標の実装
  - カスタム指標の追加
  - 評価方法の改善

### 6. 実験管理と再現性確保
- `wandb/`の設定
  - 実験の追跡
  - 結果の可視化
  - メトリクスの記録
- `src/scripts/`の整備
  - 学習スクリプトの改善
  - 予測スクリプトの実装
  - 提出スクリプトの準備
- `competition/configs/experiment/`の管理
  - 実験設定の記録
  - パラメータの管理
  - 再現性の確保

### 7. 提出準備と評価
- `competition/models/submission/`の準備
  - 提出用モデルの選択
  - モデルの最終確認
  - バックアップの確保
- `src/scripts/predict.py`の実行
  - 予測の生成
  - 結果の検証
  - 提出ファイルの準備
- `src/scripts/submit.py`の実行
  - 提出の実行
  - 結果の確認
  - フィードバックの分析

### 8. ドキュメントと整理
- `README.md`の更新
  - プロジェクトの説明
  - 使用方法の記録
  - 結果のまとめ
- `competition/notebooks/`の整理
  - ノートブックの整理
  - 結果のまとめ
  - 学びの記録
- コードの最適化
  - 不要なコードの削除
  - 再利用可能な部分の抽出
  - ドキュメントの整備

## 開発環境
- Python 3.10+
- Docker
- Weights & Biases / MLflow
- Jupyter Notebook
- Git

## セットアップ
1. リポジトリのクローン
```bash
git clone [repository-url]
```

2. 環境変数の設定
```bash
cp .env.example .env
# .envファイルを編集
```

3. コンテナの起動
```bash
docker-compose up -d
```

4. 依存関係のインストール
```bash
pip install -r requirements.txt
```

## 開発ルール
- `.cursor/rules/`ディレクトリのルールを遵守
- コミットメッセージは規約に従う
- 実験はwandb/mlflowで記録
- コードは適切にドキュメント化
- 再現性を確保
- セキュリティに配慮

## ライセンス
MIT License