# ML Competition Template

機械学習コンペティション用のテンプレートプロジェクトです。

## ディレクトリ構造と目的

```
.
├── configs/           # 設定ファイル
│   └── default.json  # モデルパラメータ、データパスなどの設定
├── data/             # データ管理
│   ├── input/        # 入力データ（train.csv, test.csv）
│   └── output/       # 出力データ（予測結果、モデル）
├── features/         # 特徴量エンジニアリング
│   ├── base.py       # 特徴量生成の基底クラス
│   └── create.py     # 特徴量生成スクリプト
├── models/          # モデル定義と学習
│   └── lgbm.py      # LightGBMモデルの実装
├── notebooks/       # 探索的データ分析と実験
│   └── eda.ipynb    # データ分析と実験用ノートブック
├── scripts/         # データ変換や前処理スクリプト
│   └── convert_to_feather.py  # データ形式変換
├── docker-compose.yml  # Docker環境設定
├── Dockerfile       # 環境構築
├── LICENSE         # ライセンス情報
├── README.md       # プロジェクト説明
├── requirements.txt # 依存関係
└── run.py          # メイン実行スクリプト
```

## 開発環境のセットアップ

1. リポジトリをクローン
```bash
git clone https://github.com/gen03/ml-competition-template.git
cd ml-competition-template
```

2. Docker環境の起動
```bash
docker compose up
```

3. Jupyter Labにアクセス
- ブラウザで `http://localhost:8888` を開く
- トークンは `docker compose logs` で確認

## 開発フロー

1. データ分析
- `notebooks/eda.ipynb` を開いてデータを確認
- 必要な分析を実施

2. 特徴量エンジニアリング
- `features/base.py` で新しい特徴量を実装
- `features/create.py` で特徴量を生成

3. モデル学習
- `configs/default.json` でパラメータを調整
- `python run.py` で学習と予測を実行

## ライセンス

MIT License