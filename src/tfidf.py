import itertools
import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import jieba  # ldkrsi/jieba-zh_TW for traditional Chinese
from scipy.spatial import distance
import networkx as nx
import matplotlib.pyplot as plt

SHOW = False
data = json.loads(open("cna-category-aipl(example).json", "r").read())
jieba.load_userdict("userdict.txt")
with open("stopwords.txt", "r") as f:
    stopwords = [word.strip("\n ") for word in f.readlines()]
texts = []
for v in data.values():
    cut_result = jieba.cut(v["text"].lower(), cut_all=False)

    cut_result = filter(lambda x: x not in stopwords, cut_result)
    texts.append(" ".join(cut_result))
"""
需要觀察分詞結果來加入字典時，可以用這個輸出
with open('cut result.txt', 'w') as f:
    f.write('\n'.join(texts))
exit(0)
"""
vectorizer = TfidfVectorizer(norm=None)
vectorizer.fit(texts)
tfidf = vectorizer.fit_transform(texts).toarray()

id_to_text = vectorizer.get_feature_names_out()
print(id_to_text, type(id_to_text), id_to_text.shape)

print(tfidf.shape)
word_cnt = {}
for news in texts:
    for word in news.split(" "):
        if word not in word_cnt:
            word_cnt[word] = 1
        else:
            word_cnt[word] += 1
        # print(word)
data = []
for i in range(len(tfidf)):
    row = []
    for id, tfidf_ in enumerate(tfidf[i]):
        # print(id,id_to_text[id])
        # print(word_cnt.get(id_to_text[id],0))
        # print(id_to_text[id], tfidf_, word_cnt.get(id_to_text[id],0))
        if tfidf_ > 10 and word_cnt.get(id_to_text[id], 0) >= 30:
            row.append(id_to_text[id])

    data.append(row)
id_to_text = {}
text_to_id = {}
for news in data:
    for word in news:
        if word not in text_to_id:
            text_to_id[word] = len(text_to_id)
            id_to_text[len(text_to_id) - 1] = word
print(id_to_text)

combinations = [list(itertools.combinations(news, 2)) for news in data]
combination_matrix = np.zeros((len(id_to_text), len(id_to_text)))
for tweet_comb in combinations:
    for comb in tweet_comb:
        combination_matrix[text_to_id[comb[0]], text_to_id[comb[1]]] += 1
        combination_matrix[text_to_id[comb[1]], text_to_id[comb[0]]] += 1

for i in range(len(id_to_text)):
    combination_matrix[i, i] /= 2

jaccard_matrix = 1 - distance.cdist(combination_matrix, combination_matrix, "jaccard")

nodes = []

for i in range(len(id_to_text)):
    for j in range(i + 1, len(id_to_text)):
        jaccard = jaccard_matrix[i, j]
        if jaccard > 0:
            nodes.append(
                [
                    id_to_text[i],
                    id_to_text[j],
                    word_cnt[id_to_text[i]],
                    word_cnt[id_to_text[j]],
                    jaccard,
                ]
            )

G = nx.Graph()
G.nodes(data=True)

for pair in nodes:
    node_x, node_y, node_x_cnt, node_y_cnt, jaccard = (
        pair[0],
        pair[1],
        pair[2],
        pair[3],
        pair[4],
    )
    if not G.has_node(node_x):
        G.add_node(node_x, count=node_x_cnt)
    if not G.has_node(node_y):
        G.add_node(node_y, count=node_y_cnt)
    if not G.has_edge(node_x, node_y):
        G.add_edge(node_x, node_y, weight=jaccard)
plt.rcParams["font.sans-serif"] = ["AR PL UMing CN"]
plt.figure(figsize=(15, 15))
pos = nx.spring_layout(G, k=0.5, iterations=1000)

node_size = [d["count"] * 10 for (n, d) in G.nodes(data=True)]
nx.draw_networkx_nodes(G, pos, node_color="cyan", alpha=1.0, node_size=node_size)
nx.draw_networkx_labels(G, pos, font_family="AR PL UMing CN")

edge_width = [d["weight"] * 10 for (u, v, d) in G.edges(data=True)]
nx.draw_networkx_edges(G, pos, alpha=0.4, edge_color="black", width=edge_width)

if SHOW:
    plt.show()
else:
    plt.savefig("output.jpg")
