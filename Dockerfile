FROM python:3.11-slim

WORKDIR /workspace

# 必要なパッケージのインストール
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Gitの設定（環境変数から取得）
ARG GIT_USER_NAME
ARG GIT_USER_EMAIL
RUN git config --global user.name "${GIT_USER_NAME}" \
    && git config --global user.email "${GIT_USER_EMAIL}"

# Pythonパッケージのインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 追加のパッケージ
RUN pip install --no-cache-dir \
    pyarrow \
    fastparquet

# Jupyter Labのインストール
RUN pip install --no-cache-dir \
    jupyterlab \
    jupytext

# ポートの公開
EXPOSE 8888

# 起動コマンド
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]