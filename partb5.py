import re
import os
import sys
import nltk
from pathlib import Path
import pandas as pd
import numpy as np
from itertools import chain
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from itertools import chain


args = sys.argv[1:]

porter = nltk.PorterStemmer()
ports = [porter.stem(x.lower()) for x in args]
args.extend(ports)


path = Path().cwd()
filepath = path.joinpath('./cricket')
files = [filepath.joinpath(x) for x in os.listdir(filepath)]

docid = pd.read_csv(path.joinpath('partb1.csv'),sep='\t')

text = []
for file in files:
    with open(file,'r',encoding='utf-8') as f:
        data = [x.strip().lower() for x in f if x.strip()]
        data= [re.sub('[^a-z -]+','',x) for x in data]
        data = [[y for y in x.split() if y] for x in data]
        totaltext = list(chain(*data))
        text.append(' '.join(totaltext))
docid['text'] = np.array(text)
docid['search'] = docid['text'].apply(lambda x: set(args) & set(x.split()) == set(args))

tfidf = TfidfVectorizer()
textx = tfidf.fit_transform(docid['text'])
docid['tfidf'] = textx.toarray().tolist()
docid = docid[docid['search'] == True]
args_tfidf = tfidf.transform([' '.join(args)]).toarray()


result = []
for x in docid[['documentID','tfidf']].values.tolist():
    ids = x[0]
    text_tfidf = np.array([[y for y in x[-1]]])
    result.append([ids,cosine_similarity(args_tfidf,text_tfidf).item()])

result = list(sorted(result,key = lambda x: x[-1], reverse=True))

print(result)