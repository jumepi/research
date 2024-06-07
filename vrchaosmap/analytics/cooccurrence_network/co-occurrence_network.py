import pandas as pd
import cupy as cp
import networkx as nx
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from tqdm import tqdm

# データの読み込み
input_file = '../../output/arxiv/csv/virtual_reality.csv'
df = pd.read_csv(input_file)

# キーワードの前処理
df['keywords'] = df['keywords'].str.lower()
df['keywords'] = df['keywords'].str.split(',')
df['keywords_str'] = df['keywords'].apply(lambda x: ' '.join(x))

# キーワードのベクトル化
vectorizer = CountVectorizer(tokenizer=lambda x: x.split(' '), lowercase=False)
X = vectorizer.fit_transform(tqdm(df['keywords_str'], desc="Vectorizing keywords"))

# CPUからGPUにデータを転送
X_gpu = cp.sparse.csr_matrix(X.toarray())

# 共起行列の作成
with tqdm(total=1, desc="Calculating co-occurrence matrix") as pbar:
    Xc_gpu = X_gpu.T @ X_gpu  # 共起行列の計算
    pbar.update(1)

# 対角成分をゼロに設定
with tqdm(total=1, desc="Setting diagonal to zero") as pbar:
    Xc_gpu.setdiag(0)
    pbar.update(1)

# CPUにデータを転送
with tqdm(total=1, desc="Transferring data to CPU") as pbar:
    Xc = Xc_gpu.get()
    pbar.update(1)

# 共起行列をNetworkXのグラフに変換
with tqdm(total=1, desc="Creating network graph") as pbar:
    G = nx.from_scipy_sparse_array(Xc)
    pbar.update(1)

# ノードラベルの設定
labels = vectorizer.get_feature_names_out()
G = nx.relabel_nodes(G, {i: labels[i] for i in range(len(labels))})

# ネットワーク図の描画
plt.figure(figsize=(14, 14))
pos = nx.spring_layout(G, k=0.1)  # レイアウトの設定
nx.draw(G, pos, with_labels=True, node_size=50, font_size=10, font_weight='bold', edge_color='gray')
plt.title('Keyword Co-occurrence Network')
plt.show()