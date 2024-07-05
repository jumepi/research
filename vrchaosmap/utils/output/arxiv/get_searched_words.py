import os
import pandas as pd

word = 'construction'
filename = 'augmented_reality'

filepath = f'{filename}.csv'
# 検索するディレクトリとファイル名の設定
search_directory = '../../../output/arxiv/csv/'
output_file = f'../../../output/arxiv/{word}.csv'


# 新しいデータフレームのリストを作成
df_list = []

# ディレクトリ内の全てのCSVファイルを検索
if filepath.endswith('.csv'):
    file_path = os.path.join(search_directory, filepath)

    # CSVファイルを読み込み
    df = pd.read_csv(file_path)

    # アブストラクトの改行を削除
    df['summary'] = df['summary'].str.replace('\n', ' ').str.replace('\r', ' ')

    # 'summary'列に'construction'が含まれる行をフィルタリング
    df_construction = df[df['summary'].str.contains(word, case=False, na=False)]


    # フィルタリングされたデータフレームをリストに追加
    if not df_construction.empty:
        df_list.append(df_construction)

# 全てのフィルタリングされたデータフレームを結合
if df_list:
    result_df = pd.concat(df_list, ignore_index=True)
    filename_out =f"{word}_{filename}"
    output_file = f'../../../output/arxiv/csv/{filename_out}.csv'
    result_df.to_csv(output_file, index=False)

    print(f"{word}を含む行を新しいファイル '{output_file}' に保存しました。")
else:
    print("該当するデータは見つかりませんでした。")