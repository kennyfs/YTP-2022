import itertools
import json

import jieba  # ldkrsi/jieba-zh_TW for traditional Chinese
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from scipy.spatial import distance
from sklearn.feature_extraction.text import TfidfVectorizer


def getImage(jsonFile, imageFile):
    data = json.loads(open(jsonFile, "r").read())
    jieba.load_userdict("userdict.txt")
    with open("stopwords.txt", "r") as f:
        stopwords = [word.strip("\n ") for word in f.readlines()]
    texts = []
    for v in data.values():
        cutResult = jieba.cut(v["text"].lower(), cut_all=False)

        cutResult = filter(lambda x: x not in stopwords, cutResult)
        texts.append(" ".join(cutResult))
    """
    需要觀察分詞結果來加入字典時，可以用這個輸出
    with open('cut result.txt', 'w') as f:
        f.write('\n'.join(texts))
    exit(0)
    """
    vectorizer = TfidfVectorizer(norm=None)
    vectorizer.fit(texts)
    tfidf = vectorizer.fit_transform(texts).toarray()

    idToText = vectorizer.get_feature_names_out()
    wordCnt = {}
    for news in texts:
        for word in news.split(" "):
            if word not in wordCnt:
                wordCnt[word] = 1
            else:
                wordCnt[word] += 1
            # print(word)
    data = []
    for i in range(len(tfidf)):
        row = []
        for id, tfidf_ in enumerate(tfidf[i]):
            if tfidf_ > 10 and wordCnt.get(idToText[id], 0) >= 40:
                row.append(idToText[id])

        data.append(row)
    idToText = {}
    textToId = {}
    for news in data:
        for word in news:
            if word not in textToId:
                textToId[word] = len(textToId)
                idToText[len(textToId) - 1] = word

    combinations = [list(itertools.combinations(news, 2)) for news in data]
    combinationMatrix = np.zeros((len(idToText), len(idToText)))
    for newsComb in combinations:
        for comb in newsComb:
            combinationMatrix[textToId[comb[0]], textToId[comb[1]]] += 1
            combinationMatrix[textToId[comb[1]], textToId[comb[0]]] += 1

    for i in range(len(idToText)):
        combinationMatrix[i, i] /= 2
    jaccardMatrix = 1 - distance.cdist(combinationMatrix, combinationMatrix, "jaccard")

    nodes = []

    for i in range(len(idToText)):
        for j in range(i + 1, len(idToText)):
            jaccard = jaccardMatrix[i, j]
            if jaccard > 0:
                nodes.append(
                    [
                        idToText[i],
                        idToText[j],
                        wordCnt[idToText[i]],
                        wordCnt[idToText[j]],
                        jaccard,
                    ]
                )

    G = nx.Graph()
    G.nodes(data=True)

    for pair in nodes:
        nodeX, nodeY, nodeXCnt, nodeYCnt, jaccard = (
            pair[0],
            pair[1],
            pair[2],
            pair[3],
            pair[4],
        )
        if not G.has_node(nodeX):
            G.add_node(nodeX, count=nodeXCnt)
        if not G.has_node(nodeY):
            G.add_node(nodeY, count=nodeYCnt)
        if not G.has_edge(nodeX, nodeY):
            G.add_edge(nodeX, nodeY, weight=jaccard)
    plt.figure(figsize=(15, 15), dpi=180)
    nodeCount = [d["count"] for (n, d) in G.nodes(data=True)]
    count75percent = np.percentile(nodeCount, 75)
    nodeSize = [d * 25 for d in nodeCount]
    degree = [d for (n, d) in nx.degree(G)]
    degree75percent = np.percentile(degree, 75)
    nodeColor = []
    for i, (n, d) in enumerate(G.nodes(data=True)):
        if d["count"] > count75percent and degree[i] >= degree75percent:
            nodeColor.append("#c94dff")
        elif d["count"] > count75percent:
            nodeColor.append("#ff7878")
        elif degree[i] > degree75percent:
            nodeColor.append("#7895ff")
        else:
            nodeColor.append("cyan")
    pos = nx.spring_layout(G, k=0.5, iterations=1000)
    nx.draw_networkx_nodes(G, pos, node_color=nodeColor, alpha=1.0, node_size=nodeSize)
    nx.draw_networkx_labels(G, pos, font_size=18, font_family="AR PL UMing CN")
    edgeWidth = [d["weight"] * 10 for (u, v, d) in G.edges(data=True)]
    nx.draw_networkx_edges(G, pos, alpha=0.4, edge_color="black", width=edgeWidth)
    plt.savefig(imageFile)


if __name__ == "__main__":
    getImage("cna-category-aipl(example).json", "aipl.jpg")
