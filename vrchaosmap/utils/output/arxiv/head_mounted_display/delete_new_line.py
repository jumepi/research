import pandas as pd

# データの読み込み
name = 'augmented_reality'
input_file = f'../../../../output/arxiv/{name}.csv'
df = pd.read_csv(input_file)

# アブストラクトの改行を削除
df['summary'] = df['summary'].str.replace('\n', ' ').str.replace('\r', ' ')

# 上書き保存
df.to_csv(input_file, index=False)

print("CSVファイルのアブストラクトの改行を削除して上書き保存しました。")
