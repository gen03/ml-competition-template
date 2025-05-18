import json
import wandb
import os
from pathlib import Path
from typing import Dict, Any, Optional

def load_wandb_config(config_path: str = "configs/wandb.json") -> Dict[str, Any]:
    """wandbの設定を読み込む"""
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"警告: {config_path}が見つかりません。デフォルト設定を使用します。")
        return {
            "project": "titanic",
            "entity": "gen03",
            "name": "default-run",
            "notes": "",
            "tags": [],
            "config": {}
        }

def init_wandb(config_path: str = "configs/wandb.json") -> wandb.run:
    """wandbを初期化する"""
    # APIキーの確認
    api_key = os.environ.get("WANDB_API_KEY")
    if not api_key:
        raise ValueError("WANDB_API_KEYが設定されていません")

    # 設定の読み込み
    config = load_wandb_config(config_path)

    # wandbの初期化
    run = wandb.init(
        project=config["project"],
        entity=config["entity"],
        name=config["name"],
        notes=config["notes"],
        tags=config["tags"],
        config=config["config"]
    )
    return run

def log_metrics(metrics: Dict[str, float], step: Optional[int] = None):
    """メトリクスをwandbに記録する"""
    try:
        wandb.log(metrics, step=step)
    except Exception as e:
        print(f"警告: メトリクスの記録に失敗しました: {str(e)}")

def log_artifact(file_path: str, name: str, type: str):
    """アーティファクトをwandbに記録する"""
    try:
        artifact = wandb.Artifact(name, type=type)
        artifact.add_file(file_path)
        wandb.log_artifact(artifact)
    except Exception as e:
        print(f"警告: アーティファクトの記録に失敗しました: {str(e)}")

def finish_wandb():
    """wandbの実行を終了する"""
    try:
        wandb.finish()
    except Exception as e:
        print(f"警告: wandbの終了に失敗しました: {str(e)}")