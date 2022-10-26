import json
from sklearn.feature_extraction.text import TfidfVectorizer
import jieba
data = json.loads(open('cna-category-aipl(example).json','r').read())
texts = [" ".join(jieba.cut(v['text'], cut_all=False)) for k, v in data.items()]
#print(texts)
#以下不確定能不能動
vectorizer = TfidfVectorizer(norm = None)
tf_idf_scores = vectorizer.fit_transform(texts)
# get vocabulary of terms
feature_names = vectorizer.get_feature_names_out()
corpus_index = [n for n in texts]

import pandas as pd

# create pandas DataFrame with tf-idf scores: Term-Document Matrix
df_tf_idf = pd.DataFrame(tf_idf_scores.T.todense(), index = feature_names, columns = corpus_index)
print(df_tf_idf)