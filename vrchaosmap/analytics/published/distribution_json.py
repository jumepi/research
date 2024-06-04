import json
import os
from collections import Counter
import matplotlib.pyplot as plt
from tqdm import tqdm

# JSONデータが格納されているファイルのパス
json_file_path = '../../output/arxiv_all_data/arxiv_all_data.json'
output_dir = '../../output/images/arxiv/all/'
os.makedirs(output_dir, exist_ok=True)
output_file_path = os.path.join(output_dir, 'number_of_publications_per_year.png')

# 出版年を保存するリスト
published_years = []

# ファイルを開く
with open(json_file_path, 'r', encoding='utf-8') as f:
    # ファイルの各行を読み込む
    for line in tqdm(f):
        # 各行をJSONデータとして解析
        data = json.loads(line)
        # 解析したデータから出版年を取得し、リストに追加
        published_year = data['versions'][0]['created'].split(' ')[3]
        published_year = int(published_year)
        # 出版年が2023でない場合のみリストに追加
        if published_year != 2024:
            published_years.append(published_year)

# 各出版年の出版数を計算
year_counts = Counter(published_years)

# 出版年とその出版数をプロット
plt.figure(figsize=(10, 6))
plt.bar(year_counts.keys(), year_counts.values())
plt.xlabel('Year')
plt.ylabel('Number of Publications')
plt.title('Number of Publications per Year')
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig(output_file_path)
plt.show()