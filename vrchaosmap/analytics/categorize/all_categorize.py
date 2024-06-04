import json
from collections import Counter
import matplotlib.pyplot as plt
from tqdm import tqdm
import os

# JSONデータが格納されているファイルのパス
json_file_path = '../../output/arxiv_all_data/arxiv_all_data.json'

output_dir = '../../output/images/arxiv/all/'
os.makedirs(output_dir, exist_ok=True)
output_file_path = os.path.join(output_dir, 'number_of_publications_per_category.png')

# カテゴリを保存するリスト
categories = []

# ファイルを開く
with open(json_file_path, 'r', encoding='utf-8') as f:
    # ファイルの各行を読み込む
    for line in tqdm(f):
        # 各行をJSONデータとして解析
        data = json.loads(line)

        # 解析したデータからカテゴリを取得し、リストに追加
        category = data['categories']
        categories.append(category)

# 各カテゴリの論文数を計算
category_counts = Counter(categories)

# カテゴリとその論文数をプロット
plt.figure(figsize=(10, 6))
plt.bar(category_counts.keys(), category_counts.values())
plt.xlabel('Category')
plt.ylabel('Number of Publications')
plt.title('Number of Publications per Category')
plt.xticks(rotation=90)
plt.tight_layout()

plt.savefig(output_file_path)

plt.show()