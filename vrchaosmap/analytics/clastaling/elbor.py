import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import AgglomerativeClustering, KMeans
import matplotlib.pyplot as plt
import seaborn as sns
import tqdm

# データの読み込み
input_file = '../../output/arxiv/csv/virtual_reality.csv'
df = pd.read_csv(input_file)

df['keywords'] = df['keywords'].str.lower()

# キーワードの前処理
df['keywords'] = df['keywords'].str.split(',')
df['keywords_str'] = df['keywords'].apply(lambda x: ' '.join(x))

# キーワードのベクトル化
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df['keywords_str'])

# エルボー法の実施
def calculate_wcss(data):
    wcss = []
    for n in tqdm.tqdm(range(1, 51)):
        kmeans = KMeans(n_clusters=n, random_state=42)
        kmeans.fit(data)
        wcss.append(kmeans.inertia_)
    return wcss

wcss = calculate_wcss(X.toarray())

# WCSSのプロット
plt.figure(figsize=(10, 6))
plt.plot(range(1, 51), wcss, marker='o')
plt.title('Elbow Method For Optimal Number of Clusters')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.grid(True)
plt.show()