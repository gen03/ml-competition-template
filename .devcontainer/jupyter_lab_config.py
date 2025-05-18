# JupyterLabの設定
c.ServerApp.token = '${JUPYTER_TOKEN}'

# Jupytextの設定
c.ContentsManager.default_jupytext_formats = "py:percent"  # デフォルトで.pyファイルのみ作成
c.ContentsManager.preferred_jupytext_formats_save = "py:percent"  # 保存形式をpercent形式に設定
c.ContentsManager.default_notebook_metadata_filter = {
    "jupytext": {
        "formats": "py:percent",
        "text_representation": {
            "extension": ".py",
            "format_name": "percent",
            "format_version": "1.3",
            "jupytext_version": "1.15.0"
        }
    }
}

# 自動保存の設定
c.ContentsManager.save_script = True  # .pyファイルを自動保存
c.ContentsManager.script_save_format = "percent"  # percent形式で保存