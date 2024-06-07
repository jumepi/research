import os
import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd
import matplotlib as mpl

# matplotlibの設定を取得
mpl.rcParams['font.family'] = 'MS Gothic'  # 'MS Gothic'をインストールされている日本語対応フォントに置き換えてください

# カテゴリデータ
input_dir = '../../output/arxiv/csv/'
name = 'mixed_reality'
file_name = f'{name}.csv'
input_file_path = input_dir + file_name

# カテゴリと日本語名の対応表
category_japanese_path = '../../input/category_japanese.csv'

# 対応表を読み込む
category_japanese_df = pd.read_csv(category_japanese_path)
category_japanese_dict = dict(zip(category_japanese_df['Category ID'], category_japanese_df['Category Name (Japanese)']))

# データを読み込む
data = pd.read_csv(input_file_path)

# カテゴリデータの整形
data['category'] = data['category'].apply(lambda x: x.replace('[', "").replace(']', "").replace('"', "").replace("'", ""))
data['category'] = data['category'].apply(lambda x: x.split(', '))

# 出版年を取得
data['year'] = pd.to_datetime(data['published']).dt.year

# 各カテゴリを日本語名に変換
data['category'] = data['category'].apply(lambda x: [category_japanese_dict.get(item, item) for item in x])

# 各カテゴリの出現回数をカウント
flat_list = [item for sublist in data['category'] for item in sublist]
counter = Counter(flat_list)
counter = dict(sorted(counter.items(), key=lambda x: x[1], reverse=True))

# 上位十項目のカテゴリを抽出
top_10_categories = list(counter.keys())[:10]

# 上位十項目のカテゴリについて各年ごとの論文数を集計
yearly_counts = {category: data[data['category'].apply(lambda x: category in x)]['year'].value_counts().sort_index() for category in top_10_categories}

# プロット
plt.figure(figsize=(12, 8))

for category, counts in yearly_counts.items():
    plt.plot(counts.index, counts.values, marker='o', label=category)

plt.xlabel('Year')
plt.ylabel('Number of Publications')
plt.title('Number of Publications per Year for Top 10 Categories')
plt.legend(loc='upper left')
plt.xticks(rotation=45)

plt.tight_layout()
os.makedirs('../../output/images/arxiv/category/', exist_ok=True)
plt.savefig(f'../../output/images/arxiv/category/{name}_top10_yearly.png')
plt.show()
