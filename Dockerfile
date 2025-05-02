# Python 3.11をベースイメージとして使用
FROM python:3.11-slim

# 必要なシステムパッケージのインストール
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# 非rootユーザー'ds'の作成
RUN useradd -m -s /bin/bash ds

# Pythonパッケージのインストール
ENV PATH="/home/ds/.local/bin:${PATH}"
RUN pip install --no-cache-dir \
    numpy==1.24.3 \
    pandas==2.0.3 \
    scikit-learn==1.3.0 \
    lightgbm==4.0.0 \
    optuna==3.3.0 \
    jupyterlab==4.0.0

# Jupyter設定
RUN mkdir -p /home/ds/.jupyter && \
    echo "c.NotebookApp.token = '${JUPYTER_TOKEN}'" > /home/ds/.jupyter/jupyter_notebook_config.py

# ユーザーの切り替えとワークディレクトリの設定
USER ds
WORKDIR /workspace

# 必要なディレクトリの作成
RUN mkdir -p /workspace/notebooks \
    /workspace/data \
    /workspace/models \
    /workspace/features \
    /workspace/configs \
    /workspace/scripts

# Jupyterのポートを公開
EXPOSE 8888

# JupyterLabを起動
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser"]