# %% [markdown]
# # Titanic: Machine Learning from Disaster
#
# ## 1. ライブラリのインポートとデータの読み込み

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import wandb
%matplotlib inline

# プロットの設定
plt.style.use('default')
sns.set_theme()
sns.set(font_scale=1.2)

# 警告を無視
import warnings
warnings.filterwarnings('ignore')

# wandbの初期化
wandb.init(project="titanic-analysis", name="eda")

# データの読み込み
train = pd.read_csv('../data/input/train.csv')
test = pd.read_csv('../data/input/test.csv')

# データの形状を確認
print('Train shape:', train.shape)
print('Test shape:', test.shape)

# wandbにデータの基本情報を記録
wandb.log({
    "train_shape": train.shape[0],
    "test_shape": test.shape[0],
    "features": train.shape[1] - 1  # ターゲット変数を除く
})

# %% [markdown]
# ## 2. データの基本情報確認

# %%
# 訓練データの基本情報
print('=== Train Data Info ===')
train.info()

# 基本統計量
train_stats = train.describe()
print('\n=== Basic Statistics ===')
print(train_stats)

# wandbに統計情報を記録
wandb.log({"train_stats": wandb.Table(dataframe=train_stats)})

# %% [markdown]
# ## 3. 欠損値の確認

# %%
# 訓練データの欠損値
train_null = train.isnull().sum()
train_null = train_null[train_null > 0]
print('=== Train Data Missing Values ===')
print(train_null)

# テストデータの欠損値
test_null = test.isnull().sum()
test_null = test_null[test_null > 0]
print('\n=== Test Data Missing Values ===')
print(test_null)

# wandbに欠損値情報を記録
wandb.log({
    "train_missing_values": dict(train_null),
    "test_missing_values": dict(test_null)
})

# %% [markdown]
# ## 4. 生存率の基本分析

# %%
# 全体の生存率
survival_rate = train['Survived'].mean()
print(f'Overall survival rate: {survival_rate:.2%}')

# 生存者数の可視化
plt.figure(figsize=(8, 6))
sns.countplot(data=train, x='Survived')
plt.title('Survival Distribution')
plt.show()

# wandbに生存率を記録
wandb.log({"survival_rate": survival_rate})

# %% [markdown]
# ## 5. 重要な特徴量の分析

# %%
# 性別と生存率
plt.figure(figsize=(10, 6))
sns.barplot(data=train, x='Sex', y='Survived')
plt.title('Survival Rate by Sex')
plt.show()

# 性別ごとの生存率を表示
sex_survival = train.groupby('Sex')['Survived'].mean()
print('\nSurvival Rate by Sex:')
print(sex_survival)

# wandbに性別ごとの生存率を記録
wandb.log({"sex_survival": dict(sex_survival)})

# %%
# 客室クラスと生存率
plt.figure(figsize=(10, 6))
sns.barplot(data=train, x='Pclass', y='Survived')
plt.title('Survival Rate by Passenger Class')
plt.show()

# クラスごとの生存率を表示
class_survival = train.groupby('Pclass')['Survived'].mean()
print('\nSurvival Rate by Class:')
print(class_survival)

# wandbにクラスごとの生存率を記録
wandb.log({"class_survival": dict(class_survival)})

# %%
# 年齢分布と生存率
plt.figure(figsize=(12, 5))

# 生存者と死亡者の年齢分布
plt.subplot(1, 2, 1)
sns.kdeplot(data=train, x='Age', hue='Survived', multiple="layer")
plt.title('Age Distribution by Survival')

# 年齢帯ごとの生存率
plt.subplot(1, 2, 2)
train['AgeBin'] = pd.qcut(train['Age'], 5)
sns.barplot(data=train, x='AgeBin', y='Survived')
plt.xticks(rotation=45)
plt.title('Survival Rate by Age Groups')

plt.tight_layout()
plt.show()

# wandbに年齢帯ごとの生存率を記録
age_survival = train.groupby('AgeBin')['Survived'].mean()
wandb.log({"age_survival": dict(age_survival)})

# %% [markdown]
# ## 6. 相関分析

# %%
# 数値変数の相関行列
numeric_cols = train.select_dtypes(include=['int64', 'float64']).columns
corr_matrix = train[numeric_cols].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
plt.title('Correlation Matrix of Numeric Features')
plt.show()

# wandbに相関行列を記録
wandb.log({"correlation_matrix": wandb.Table(dataframe=corr_matrix)})

# %%
# wandbの終了
wandb.finish()