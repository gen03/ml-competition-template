# 軽量なPythonイメージを使用
FROM python:3.11-slim

# 作業ディレクトリの設定
WORKDIR /workspace

# 必要なパッケージのインストール
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# mlユーザーの作成
RUN useradd -m -s /bin/bash ml && \
    chown -R ml:ml /workspace

# Gitの設定（環境変数から取得）
ARG GIT_USER_NAME
ARG GIT_USER_EMAIL
RUN git config --global user.name "${GIT_USER_NAME}" \
    && git config --global user.email "${GIT_USER_EMAIL}"

# 基本的なデータサイエンスパッケージのインストール
RUN pip install --no-cache-dir \
    numpy \
    pandas \
    scikit-learn \
    matplotlib \
    seaborn \
    jupyterlab \
    jupytext

# 追加のパッケージのインストール
COPY requirements.txt /workspace/
RUN pip install --no-cache-dir -r /workspace/requirements.txt

# ポートの公開
EXPOSE 8888

# mlユーザーに切り替え
USER ml

# 起動コマンド
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=${JUPYTER_TOKEN}"]