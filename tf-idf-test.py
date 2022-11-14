import json
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer
import jieba # ldkrsi/jieba-zh_TW for traditional Chinese
data = json.loads(open('cna-category-aipl(example).json','r').read())
texts = [" ".join(jieba.cut(v['text'], cut_all=False)) for v in data.values()]
vectorizer = CountVectorizer(token_pattern=r'\b\w+\b')
vectorizer.fit(texts)
X = vectorizer.transform(texts)

tfidf_transformer = TfidfTransformer()
tfidf_transformer.fit(X.toarray())

id_to_text = vectorizer.get_feature_names_out()
print(id_to_text,type(id_to_text),id_to_text.shape)

tfidf = tfidf_transformer.transform(X).toarray()
data = []
for i in range(len(tfidf)):
    row = [id for id,tfidf_ in enumerate(tfidf[i]) if tfidf_>0.2]
    data.append(row)
#處理cooccurrence matrix（未來用networkx的話就是直接連邊）
cooccurrence = np.zeros((len(id_to_text),len(id_to_text)))
for row in data:
    for word in row:
        for word2 in range(len(row)):
            if word2 in row and word!=word2:
                cooccurrence[word,word2] += 1
#印出一些關鍵字做參考
for id in data[0]:
    print(id_to_text[id])