import requests
import feedparser
import os
import csv
from tqdm import tqdm

# arXivのAPIエンドポイント
api_endpoint = 'http://export.arxiv.org/api/query?'

# 検索クエリの設定
query = '"mixed reality"'
query_name = query.replace(' ', '_')
output_dir = f'../output/arxiv/'
output_file_name = f'{query_name}.csv'
os.makedirs(output_dir, exist_ok=True)
output_file_path = os.path.join(output_dir, output_file_name)

# CSVファイルに書き込む処理を追加する
with open(output_file_path, 'w', newline='') as csvfile:
    fieldnames = ['title', 'summary', 'authors', 'published', 'link']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for i in tqdm(range(0, 5000, 100)):
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
            writer.writerow({
                'title': entry.title,
                'summary': entry.summary,
                'authors': [author.name for author in entry.authors],
                'published': entry.published,
                'link': entry.link
            })