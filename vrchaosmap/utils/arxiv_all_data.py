import requests
import feedparser
import csv
import os
import time
from tqdm import tqdm

# arXivのAPIエンドポイント
api_endpoint = 'http://export.arxiv.org/api/query?'

# 検索クエリの設定
query = 'all'

# 出力ディレクトリとファイル名の設定
output_dir = '../../output/arxiv/'
os.makedirs(output_dir, exist_ok=True)
output_file_path = os.path.join(output_dir, 'all_data.csv')

# CSVファイルに書き込む処理を追加する
with open(output_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['published', 'title', 'category']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for i in tqdm(range(0, 50000000, 100)):
        # APIリクエストを送信
        response = requests.get(api_endpoint, params={
            'search_query': query,
            'start': i,
            'max_results': 1000
        })
        feed = feedparser.parse(response.text)
        if feed.entries == []:
            break

        for entry in feed.entries:
            # 出版年とタイトルを取得
            publication_year = entry.published.split('-')[0]
            title = entry.title
            # カテゴリを取得
            category = entry.arxiv_primary_category['term']

            # CSVファイルに書き込む
            writer.writerow({
                'published': publication_year,
                'title': title,
                'category': category
            })

        # APIの使用制限を避けるために、リクエスト間に待機時間を設ける
        time.sleep(3)