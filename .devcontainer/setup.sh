#!/bin/bash

# 環境変数の読み込み
if [ -f .env ]; then
    # コメント行を除外しつつ、変数を読み込む
    while IFS= read -r line; do
        # 空行とコメント行をスキップ
        [[ -z "$line" || "$line" =~ ^[[:space:]]*# ]] && continue
        # 変数をエクスポート
        export "$line"
    done < .env
fi

# Git設定
if [ ! -z "$GIT_USER_NAME" ] && [ ! -z "$GIT_USER_EMAIL" ]; then
    git config --global user.name "$GIT_USER_NAME"
    git config --global user.email "$GIT_USER_EMAIL"
    echo "Git configuration set successfully"
else
    echo "Warning: GIT_USER_NAME or GIT_USER_EMAIL not set in .env"
fi

# Weights & Biases設定
if [ ! -z "$WANDB_API_KEY" ]; then
    # APIキーを直接指定してログイン
    echo "Logging in to Weights & Biases..."
    wandb login "$WANDB_API_KEY" --relogin
    # エンティティが設定されている場合は環境変数として設定
    if [ ! -z "$WANDB_ENTITY" ]; then
        export WANDB_ENTITY="$WANDB_ENTITY"
        echo "WANDB_ENTITY set to: $WANDB_ENTITY"
    fi
    # ログイン状態を確認
    if wandb status | grep -q "api_key: null"; then
        echo "Warning: Weights & Biases login failed"
        exit 1
    else
        echo "Weights & Biases login successful"
    fi
else
    echo "Warning: WANDB_API_KEY not set in .env"
    exit 1
fi

# Kaggle設定
if [ ! -z "$KAGGLE_USERNAME" ] && [ ! -z "$KAGGLE_KEY" ]; then
    echo "Setting up Kaggle configuration..."
    # Kaggleの認証情報ディレクトリを作成
    mkdir -p ~/.kaggle
    # 環境変数から認証情報を取得して設定
    echo "{\"username\":\"$KAGGLE_USERNAME\",\"key\":\"$KAGGLE_KEY\"}" > ~/.kaggle/kaggle.json
    # 権限を設定
    chmod 600 ~/.kaggle/kaggle.json
    echo "Kaggle configuration set successfully"
else
    echo "Warning: KAGGLE_USERNAME or KAGGLE_KEY not set in .env"
    exit 1
fi

# 権限設定（.gitディレクトリを除外）
find /workspace -not -path "*/\.git/*" -exec chown ml:ml {} \;