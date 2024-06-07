import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime

# データの読み込み
input_file = '../../output/arxiv/csv/virtual_reality.csv'
df = pd.read_csv(input_file)

# 日付をdatetime形式に変換
df['published'] = pd.to_datetime(df['published'])

# 年ごとのキーワード出現頻度
df['year'] = df['published'].dt.year

# すべてlowercaseに変換
df['keywords'] = df['keywords'].str.lower()
# キーワード出現頻度を計算
keyword_yearly_counts = df['keywords'].str.split(',').explode().groupby(df['year']).value_counts().unstack(fill_value=0)

# 全期間でのキーワードの出現頻度を計算
total_keyword_counts = keyword_yearly_counts.sum().sort_values(ascending=False)

# virtual reality, Virtual Reality Virtual reality Augmented reality Augmented Reality VR を除外
total_keyword_counts = total_keyword_counts.drop(['virtual reality', 'vr', 'virtual reality (vr)'])

# 上位N個の頻出キーワードを選択
top_n = 10
top_keywords = total_keyword_counts.head(top_n).index

# 頻出キーワードのトレンドをプロット
plt.figure(figsize=(14, 8))
for keyword in top_keywords:
    plt.plot(keyword_yearly_counts.index, keyword_yearly_counts[keyword], label=keyword)


plt.xlabel('Year')
plt.ylabel('Frequency')
plt.title('Trend of Top Keywords Over Years')
plt.legend(title='Keywords')
plt.grid(True)
plt.show()
