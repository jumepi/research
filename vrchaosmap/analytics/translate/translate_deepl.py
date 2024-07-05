import pandas as pd
import deepl
from tqdm import tqdm

# DeepLの認証キー
auth_key = "533100d0-6fee-46ee-b9a6-75f09be3c14e:fx"  # Replace with your key
translator = deepl.Translator(auth_key)

# CSVファイルのパス
file_name = 'construction_augmented_reality'  # 適切なファイル名に置き換えてください
input_file_path = f'../../output/arxiv/csv/{file_name}.csv'

# CSVファイルを読み込む
df = pd.read_csv(input_file_path)

# summary列を日本語に翻訳し、新しい列JAsummaryに追加する
translated_summaries = []
for summary in tqdm(df['summary']):
    result = translator.translate_text(summary, target_lang="JA")
    translated_summaries.append(result.text)

df['JAsummary'] = translated_summaries

# CSVファイルに書き戻す
df.to_csv(input_file_path, index=False)
