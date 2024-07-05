import os

import matplotlib.pyplot as plt
import japanize_matplotlib
from collections import Counter
import pandas as pd

# matplotlibの設定を取得

# カテゴリデータ
input_dir = '../../output/arxiv/csv/'
name = 'augmented_reality'
file_name = f'{name}.csv'
input_file_path = input_dir + file_name

# カテゴリと日本語名の対応表
category_japanese_path = '../../input/category_japanese.csv'

# 対応表を読み込む
category_japanese_df = pd.read_csv(category_japanese_path)
category_japanese_dict = dict(zip(category_japanese_df['Category ID'], category_japanese_df['Category Name (Japanese)']))

# データを読み込む
data = pd.read_csv(input_file_path)

data = [d.replace('[', "").replace(']', "").replace('"', "").replace("'", "") for d in data['category']]
# , or ; でデータを分割
data = [d.split(', ' or '; ') for d in data]
# データをフラットなリストに変換
flat_list = [item for sublist in data for item in sublist]

# カテゴリを日本語名に変換
flat_list = [category_japanese_dict.get(item, item) for item in flat_list if item in category_japanese_dict]

# 各カテゴリの出現回数をカウント
counter = Counter(flat_list)

# カウント結果をソートして上位10項目を抽出
top_n = 30
counter = dict(sorted(counter.items(), key=lambda x: x[1], reverse=True)[:top_n])

# カウント結果をラベルと値に分ける
labels = list(counter.keys())
values = list(counter.values())

# グラフを描画
plt.figure(figsize=(10, 6))
plt.bar(labels, values)
plt.xlabel('Category')
plt.ylabel('Number of Publications')
plt.title('Number of Publications per Category')
plt.xticks(rotation=90)

plt.tight_layout()
os.makedirs('../../output/images/arxiv/category/', exist_ok=True)
plt.savefig(f'../../output/images/arxiv/category/{name}.png')
plt.show()