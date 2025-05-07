# ML Competition Template

機械学習コンペティション用のテンプレートプロジェクトです。Dockerコンテナを使用した開発環境を提供し、Jupyter LabとPythonの統合環境を構築します。

## 機能

- Dockerコンテナベースの開発環境
- Jupyter Lab統合
- Weights & Biasesによる実験管理
- モジュール化されたプロジェクト構造
- 自動化された環境構築

## 必要条件

- Docker
- Cursor IDE（またはVS Code + Dev Containers拡張）

## クイックスタート

1. リポジトリのクローン:
```bash
git clone [repository-url]
cd ml-competition-template
```

2. 環境変数の設定:
`.env`ファイルを作成し、以下の内容を設定:
```
JUPYTER_TOKEN=your_token
JUPYTER_PASSWORD=your_password
PYTHONPATH=/workspace
```

3. コンテナの起動:
- Cursor IDEでプロジェクトを開く
- コマンドパレット（Cmd+Shift+P）を開く
- 「Dev Containers: Rebuild and Reopen in Container」を選択

## プロジェクト構造

```
.
├── .devcontainer/     # コンテナ設定
├── data/             # データディレクトリ
│   ├── input/       # 入力データ
│   └── output/      # 出力データ
├── notebooks/        # Jupyter notebooks
├── features/         # 特徴量エンジニアリング
├── models/          # モデル定義
├── configs/         # 設定ファイル
├── scripts/         # ユーティリティスクリプト
└── requirements.txt  # 依存パッケージ
```

## 開発環境

- Python 3.11
- Jupyter Lab
- 主要パッケージ:
  - numpy
  - pandas
  - scikit-learn
  - lightgbm
  - optuna
  - wandb

## 使用方法

1. Jupyter Labの起動:
- コンテナ起動後、自動的にJupyter Labが起動
- ブラウザで`http://localhost:8888`にアクセス
- トークン認証でログイン

2. コードの実行:
- `.py`ファイルでのセル実行（`# %%`で区切られたセル）
- Jupyter Notebookの編集と実行
- プロットの表示

## 実験管理

Weights & Biasesを使用して実験を管理:
- メトリクスの追跡
- ハイパーパラメータの管理
- 結果の可視化

## ライセンス

MIT License