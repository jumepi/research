import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from tqdm import tqdm
import os

# データの読み込み
name = 'virtual_reality'
input_file = f'../../output/arxiv/csv/{name}.csv'
df = pd.read_csv(input_file)

# キーワードの前処理
df['keywords'] = df['keywords'].str.lower()
df['keywords'] = df['keywords'].str.split(',')
df['keywords_str'] = df['keywords'].apply(lambda x: ','.join(x))

# キーワードのベクトル化
vectorizer = CountVectorizer(tokenizer=lambda x: x.split(','), lowercase=False)
X = vectorizer.fit_transform(tqdm(df['keywords_str'], desc="Vectorizing keywords"))

# キーワードの出現頻度を計算
keyword_counts = np.asarray(X.sum(axis=0)).flatten()
keyword_indices = np.argsort(keyword_counts)[::-1]

# 出現頻度上位N個のキーワードを選択
N = 80  # 表示するキーワードの数を設定
top_indices = keyword_indices[:N]
top_keywords = [vectorizer.get_feature_names_out()[i] for i in top_indices]

# 上位N個のキーワードのベクトルを再計算
vectorizer_top = CountVectorizer(vocabulary=top_keywords, tokenizer=lambda x: x.split(','), lowercase=False)
X_top = vectorizer_top.fit_transform(df['keywords_str'])

# 共起行列の作成
with tqdm(total=1, desc="Calculating co-occurrence matrix") as pbar:
    Xc_top = (X_top.T @ X_top).toarray()  # 共起行列の計算
    pbar.update(1)

# 対角成分をゼロに設定
with tqdm(total=1, desc="Setting diagonal to zero") as pbar:
    np.fill_diagonal(Xc_top, 0)
    pbar.update(1)

# 共起行列をNetworkXのグラフに変換
with tqdm(total=1, desc="Creating network graph") as pbar:
    G_top = nx.from_numpy_array(Xc_top)
    pbar.update(1)

# エッジの重み（共起数）を計算
weights = {e: G_top[e[0]][e[1]]['weight'] for e in G_top.edges}

# 閾値を設定し、エッジをフィルタリング
threshold = 0.5  # この値を調整して表示するエッジの数を制御
filtered_edges = [(u, v, w) for u, v, w in G_top.edges(data=True) if w['weight'] >= threshold]
G_filtered = nx.Graph()
G_filtered.add_edges_from(filtered_edges)

# ノードラベルの設定
labels_top = vectorizer_top.get_feature_names_out()
G_filtered = nx.relabel_nodes(G_filtered, {i: labels_top[i] for i in range(len(labels_top))})

# ノードサイズを設定（出現頻度に基づく）
node_sizes = [keyword_counts[top_indices[i]] * 10 for i in range(len(top_indices)) if labels_top[i] in G_filtered.nodes]

# エッジの太さを設定（共起の強さに基づく）
edge_weights = [w['weight'] * 0.2 for u, v, w in G_filtered.edges(data=True)]

# コミュニティの検出
communities = nx.algorithms.community.greedy_modularity_communities(G_filtered)
community_map = {}
for i, comm in enumerate(communities):
    for node in comm:
        community_map[node] = i

# ノードの色をコミュニティごとに設定
colors = [community_map[node] for node in G_filtered.nodes]

# ネットワーク図の描画
plt.figure(figsize=(14, 14))
pos = nx.spring_layout(G_filtered, k=0.1)  # レイアウトの設定
nx.draw(G_filtered, pos, with_labels=True, node_size=node_sizes, node_color=colors, cmap=plt.cm.rainbow, font_size=10, font_weight='bold', edge_color='gray', width=edge_weights)
plt.title('Keyword Co-occurrence Network (Filtered and Colored by Community)')

os.makedirs('../../output/images/cooccurrence_network/', exist_ok=True)
plt.savefig(f'../../output/images/cooccurrence_network/{name}_Filtered_and_Colored_by_Community.png')
plt.show()
