import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import AgglomerativeClustering
import matplotlib.pyplot as plt
import seaborn as sns

# データの読み込み
input_file = '../../output/arxiv/csv/virtual_reality.csv'
df = pd.read_csv(input_file)

df['keywords'] = df['keywords'].str.lower()

# キーワードをベクトル化
vectorizer = CountVectorizer(tokenizer=lambda x: x.split(','), lowercase=False)
X = vectorizer.fit_transform(df['keywords'].apply(lambda x: ','.join(x.split(','))))

# コサイン類似度の計算
cosine_sim = cosine_similarity(X)

# 階層的クラスタリングの実行
clustering = AgglomerativeClustering(n_clusters=10, metric='precomputed', linkage='complete')
clusters = clustering.fit_predict(1 - cosine_sim)

# クラスタの割り当て
df['cluster'] = clusters

# クラスタごとの代表キーワードを表示
def get_top_keywords(cluster, n_terms=10):
    cluster_ids = df[df['cluster'] == cluster].index
    all_keywords = ','.join(df.loc[cluster_ids, 'keywords'].apply(lambda x: ','.join(x.split(','))))
    count = CountVectorizer(tokenizer=lambda x: x.split(','), lowercase=False).fit([all_keywords])
    keywords_count = count.transform([all_keywords]).toarray().sum(axis=0)
    keywords_freq = dict(zip(count.get_feature_names_out(), keywords_count))
    top_keywords = sorted(keywords_freq.items(), key=lambda x: x[1], reverse=True)[:n_terms]
    return top_keywords

n_terms = 10
for i in range(clustering.n_clusters):
    print(f"Cluster {i}:")
    print(get_top_keywords(i, n_terms))
    print("\n")

# クラスタリング結果の可視化（例: 論文数をクラスタごとに表示）
plt.figure(figsize=(10, 6))
sns.countplot(x='cluster', data=df)
plt.xlabel('Cluster')
plt.ylabel('Number of Papers')
plt.title('Number of Papers per Cluster')
plt.show()
