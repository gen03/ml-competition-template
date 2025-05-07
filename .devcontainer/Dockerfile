# Python 3.11をベースイメージとして使用
FROM python:3.11-slim

# Git設定用の引数
ARG GIT_USER_NAME
ARG GIT_USER_EMAIL

# 環境変数の設定
ENV GIT_USER_NAME=${GIT_USER_NAME}
ENV GIT_USER_EMAIL=${GIT_USER_EMAIL}

# 必要なシステムパッケージのインストール
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    unzip \
    wget \
    gnupg \
    ca-certificates \
    openssh-client \
    && rm -rf /var/lib/apt/lists/*

# 非rootユーザー'ml'の作成
RUN useradd -m -s /bin/bash ml

# Pythonパッケージのインストール
ENV PATH="/home/ml/.local/bin:${PATH}"
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Jupyter設定
RUN mkdir -p /home/ml/.jupyter
RUN echo 'c.NotebookApp.allow_origin = "*"' > /home/ml/.jupyter/jupyter_notebook_config.py && \
    echo 'c.ServerApp.allow_origin = "*"' >> /home/ml/.jupyter/jupyter_notebook_config.py && \
    echo 'c.NotebookApp.token = ""' >> /home/ml/.jupyter/jupyter_notebook_config.py && \
    echo 'c.ServerApp.token = ""' >> /home/ml/.jupyter/jupyter_notebook_config.py && \
    echo 'c.NotebookApp.ip = "0.0.0.0"' >> /home/ml/.jupyter/jupyter_notebook_config.py && \
    echo 'c.ServerApp.ip = "0.0.0.0"' >> /home/ml/.jupyter/jupyter_notebook_config.py

RUN chown -R ml:ml /home/ml/.jupyter

# VS Code Serverのインストールに必要なディレクトリと権限の設定
RUN mkdir -p /home/ml/.vscode-server \
    && chown -R ml:ml /home/ml/.vscode-server

# SSH設定
RUN mkdir -p /home/ml/.ssh && \
    chmod 700 /home/ml/.ssh && \
    chown -R ml:ml /home/ml/.ssh

# Git設定
RUN git config --global user.name "${GIT_USER_NAME}" && \
    git config --global user.email "${GIT_USER_EMAIL}" && \
    git config --global --add safe.directory /workspace

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
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--NotebookApp.token=${JUPYTER_TOKEN}"]