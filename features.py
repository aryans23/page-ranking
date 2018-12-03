import os
from pprint import pprint
from collections import Counter
import nltk
from nltk.tokenize import RegexpTokenizer
import numpy as np
from nltk.corpus import stopwords
import re
from sklearn.feature_extraction import DictVectorizer

def get_features(verbose=False):
	ps = nltk.stem.PorterStemmer()
	tokenizer = RegexpTokenizer(r'\w+')
	bag = Counter()
	token_list = []

	for filename in os.listdir("./dump-texts"):
		file = os.path.join("dump-texts",filename)
		if verbose:
			print "PROCESSED " + file
		with open(file, 'r') as f:
			text = f.read().lower().decode('utf-8')
			text = re.sub(r'\d+', '', text)
			filtered_text = [w for w in tokenizer.tokenize(text) if w not in stopwords.words('english')]
			tokens = [ps.stem(x) for x in filtered_text]
			token_list.append(tokens)
			bag.update(tokens)

	weights = {}
	i = 10
	if verbose:
		print "\nPrinting most common tokens..."
	for x in bag.most_common(20):
	    if verbose:
	    	print("# " + str(x[0]) + ': ' + str(x[1]))
	    weights[str(x[0])] = i
	    i = i-0.5

	if verbose:
		print "\nPrinting weight dictionary..."
	for s,w in weights.items():
		if verbose:
			print s + ": " + str(w)

	print "************* Features computed!"
	return weights