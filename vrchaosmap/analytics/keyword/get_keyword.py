from openai import OpenAI
import pandas as pd
from tqdm import tqdm
import os
from dotenv import load_dotenv

# .envファイルを読み込みます
load_dotenv()

client = OpenAI()

# OpenAI APIキーを設定します
OpenAI.api_key = os.getenv('OPENAI_API_KEY')


def extract_keywords(title, abstract):
    # Abstractの改行を取り除く
    abstract = " ".join(abstract.splitlines())

    prompt = f"Extract up to ten technical terms from the following title and abstract. Focus on terms necessary for categorizing the paper and provide them as a comma-separated list:\n\nTitle:\n\n{title}\n\nAbstract:\n\n{abstract}\n\nKeywords:"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": prompt}
        ]
    )

    # 結果を抽出
    keywords = response.choices[0].message.content.strip()
    return keywords.split(',')


# CSVファイルを読み込みます
input_file = '../../output/arxiv/csv/virtual_reality.csv'
df = pd.read_csv(input_file)

# 各行のサマリーからキーワードを抽出してリストに追加します
for index, row in tqdm(df.iterrows(), total=len(df)):
    abstract = row['summary']
    title = row['title']
    keywords = extract_keywords(title, abstract)
    keywords_str = ','.join([kw.strip() for kw in keywords])
    df.at[index, 'keywords'] = keywords_str

    # 変更をファイルに書き込む
    df.to_csv(input_file, index=False)

print("処理が完了しました。ファイルが更新されました。")
