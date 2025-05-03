# Python 3.11をベースイメージとして使用
FROM python:3.11-slim

# 必要なシステムパッケージのインストール
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# 非rootユーザー'ml'の作成
RUN useradd -m -s /bin/bash ml

# Pythonパッケージのインストール
ENV PATH="/home/ml/.local/bin:${PATH}"
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Jupyter設定
RUN mkdir -p /home/ml/.jupyter && \
    echo "c.NotebookApp.token = '${JUPYTER_TOKEN}'" > /home/ml/.jupyter/jupyter_notebook_config.py

# ユーザーの切り替えとワークディレクトリの設定
USER ml
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