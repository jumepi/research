import json
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
from tqdm import tqdm
import os

# JSONデータが格納されているファイルのパス
json_file_path = '../../output/arxiv_all_data/arxiv_all_data.json'

output_dir = '../../output/images/arxiv/all/'
os.makedirs(output_dir, exist_ok=True)
output_file_path = os.path.join(output_dir, 'number_of_publications_per_year_for_selected_and_all_topics.png')

# 出版年とトピック名を保存する辞書
published_years_topics = defaultdict(list)

# ファイルを開く
with open(json_file_path, 'r', encoding='utf-8') as f:
    # ファイルの各行を読み込む
    for i, line in enumerate(tqdm(f)):

        # 各行をJSONデータとして解析
        data = json.loads(line)

        # 解析したデータからタイトルと抄録を取得
        title = data['title']
        abstract = data['abstract']
        # 出版年を取得し、辞書に追加
        published_year = data['versions'][0]['created'].split(' ')[3]
        published_year = int(published_year)
        # タイトルまたは抄録が指定したトピックと全文一致するか確認
        for topic in ['augmented reality', 'virtual reality', 'mixed reality']:
            # dataのどこかにtopicが含まれているか確認
            if topic in title.lower() or topic in abstract.lower():
                # 出版年が2024でない場合のみ辞書に追加
                if published_year != 2024:
                    published_years_topics[topic].append(published_year)
        published_years_topics["all"].append(published_year)

print(len(published_years_topics['augmented reality']))
print(len(published_years_topics['virtual reality']))
print(len(published_years_topics['mixed reality']))
print(len(published_years_topics['all paper']))

# 出版年とその出版数をプロット
plt.figure(figsize=(10, 6))

colors = ['b', 'g', 'r']
for color, (topic, years) in tqdm(zip(colors, published_years_topics.items())):
    years = sorted(years)
    year_counts = Counter(years)
    years = list(year_counts.keys())
    counts = list(year_counts.values())

    # Plot the data
    plt.plot(years, counts, color=color, marker='o', label=topic)

plt.xlabel('Year')
plt.ylabel('Number of Publications')
plt.title('Number of Publications per Year for Selected Topics')
plt.legend()
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig(output_file_path)
plt.show()