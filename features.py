import os
from pprint import pprint
from collections import Counter
import nltk
from nltk.tokenize import RegexpTokenizer
import numpy as np
from nltk.corpus import stopwords
import re
from sklearn.feature_extraction import DictVectorizer

ps = nltk.stem.PorterStemmer()
tokenizer = RegexpTokenizer(r'\w+')
bag = Counter()
token_list = []

for filename in os.listdir("./dump-texts"):
	file = os.path.join("dump-texts",filename)
	print "PROCESSED " + file
	with open(file, 'r') as f:
		text = f.read().lower().decode('utf-8')
		text = re.sub(r'\d+', '', text)
		filtered_text = [w for w in tokenizer.tokenize(text) if w not in stopwords.words('english')]
		tokens = [ps.stem(x) for x in filtered_text]
		token_list.append(tokens)
		bag.update(tokens)

i = 1
for x in bag.most_common(20):
    print(str(i) + ' ' + str(x[0]) + ' ' + str(x[1]))
    i = i+1

token_counter = []
for t in token_list:
    token_counter.append(dict(Counter(t)))
vec = DictVectorizer()
feature_vectors = vec.fit_transform(token_counter)
print feature_vectors.shape
