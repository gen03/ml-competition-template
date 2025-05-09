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

3. JupytextによるNotebook管理:
- 初期設定（1回のみ）:
```bash
# NotebookとPythonファイルのペアを作成
jupytext --set-formats ipynb,py:percent notebooks/your_notebook.ipynb
```
- 自動同期:
  - `.ipynb`ファイルはGitで無視され、`.py`ファイルのみをコミット
  - 保存時に自動的に同期
- Kaggleへのアップロード:
```bash
# PythonファイルからNotebookを生成
jupytext --to ipynb notebooks/your_notebook.py
```

## 実験管理

Weights & Biasesを使用して実験を管理:
- メトリクスの追跡
- ハイパーパラメータの管理
- 結果の可視化

### Wandb設定手順

1. インストールと初期設定:
```bash
# Wandbのインストール（requirements.txtに含まれています）
pip install wandb

# Wandbへのログイン
wandb login
# API Keyを入力してください
```

2. API Keyの取得:
   - [Weights & Biases](https://wandb.ai/)にアカウント登録
   - プロフィール設定からAPI Keyを取得

3. 環境変数の設定:
```bash
# ローカル環境での設定
echo "WANDB_API_KEY=your_api_key" >> .env
echo "WANDB_PROJECT=titanic" >> .env
echo "WANDB_ENTITY=your_username" >> .env
```

4. Kaggle環境での設定:
   - Kaggle Notebookの「Add-ons」→「Secrets」から設定
   - キー名: `WANDB_API_KEY`
   - 値: 取得したAPI Key

5. 使用例:
```python
import wandb

# プロジェクトの初期化
run = wandb.init(
    # チーム名またはユーザー名
    entity="your-username",
    # プロジェクト名
    project="titanic",
    # 実行名（オプション）
    name="lgbm-baseline",
    # ハイパーパラメータとメタデータ
    config={
        "learning_rate": 0.05,
        "n_estimators": 400,
        "random_seed": 42
    },
    # タグ付け（オプション）
    tags=["baseline", "lightgbm"]
)

# メトリクスの記録
wandb.log({
    "fold": k,
    "auc": auc,
    "loss": loss
})

# ファイルの保存
wandb.save("submission.csv")

# 実験の終了
run.finish()
```

6. 主な機能:
   - メトリクスの追跡と可視化
   - ハイパーパラメータの管理
   - 実験結果の比較
   - モデルの保存と管理
   - チームでの実験共有

7. ダッシュボード:
   - [Weights & Biases](https://wandb.ai/)にアクセス
   - プロジェクトページで実験結果を確認
   - メトリクス、ハイパーパラメータ、システム情報を可視化

## ライセンス

MIT License