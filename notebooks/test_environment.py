# %% [markdown]
# # 環境確認テスト

# %%
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#import wandb

# %%
# Pythonバージョンとパスの確認
print(f"Python version: {sys.version}")
print(f"Python path: {sys.path}")

# %%
# 主要パッケージのバージョン確認
print(f"NumPy version: {np.__version__}")
print(f"Pandas version: {pd.__version__}")

# %%
# 簡単なプロットの作成
plt.figure(figsize=(8, 6))
x = np.linspace(0, 10, 100)
plt.plot(x, np.sin(x))
plt.title("Test Plot")
plt.show()
# %%

