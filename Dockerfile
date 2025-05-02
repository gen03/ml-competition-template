# Python 3.11をベースイメージとして使用
FROM python:3.11-slim

# 必要なシステムパッケージのインストール
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# 非rootユーザー'kaggle'の作成
RUN useradd -m -s /bin/bash kaggle

# Pythonパッケージのインストール
ENV PATH="/home/kaggle/.local/bin:${PATH}"
RUN pip install --no-cache-dir \
    numpy \
    pandas \
    scikit-learn \
    lightgbm \
    optuna \
    jupyterlab \
    kaggle \
    matplotlib \
    seaborn

# Jupyter設定
RUN mkdir -p /home/kaggle/.jupyter && \
    echo "c.NotebookApp.token = '${JUPYTER_TOKEN}'" > /home/kaggle/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.password = '${JUPYTER_PASSWORD}'" >> /home/kaggle/.jupyter/jupyter_notebook_config.py

# ユーザーの切り替えとワークディレクトリの設定
USER kaggle
WORKDIR /workspace

# Jupyterのポートを公開
EXPOSE 8888

# JupyterLabを起動
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]