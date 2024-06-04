import pandas as pd
import matplotlib.pyplot as plt
import os

# ファイル名のリストを作成
file_names = ['augmented_reality', 'virtual_reality', 'mixed_reality']

# 出力ディレクトリを作成
output_dir = '../output/images/arxiv/'
os.makedirs(output_dir, exist_ok=True)

plt.figure(figsize=(10, 6))

# 各ファイルを順番に読み込む
for file_name in file_names:
    input_file_path = f'../output/arxiv/{file_name}.csv'

    # CSVファイルを読み込む
    df = pd.read_csv(input_file_path, encoding='latin1')

    # 'published'列から年を抽出
    df['year'] = pd.to_datetime(df['published']).dt.year


    # 年が2023以下の行だけを保持
    df = df[df['year'] <= 2023]

    # 年ごとの出版数を計算
    publications_per_year = df['year'].value_counts().sort_index()

    # グラフをプロット
    publications_per_year.plot(kind='line', label=file_name)

# グラフの設定
plt.title('Number of Publications per Year')
plt.xlabel('Year')
plt.ylabel('Number of Publications')
plt.legend()

# グラフを画像として保存
plt.savefig(f'../output/images/arxiv/combined.png')

plt.show()