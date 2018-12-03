from features import get_features
import os
from nltk.tokenize import RegexpTokenizer
import re
import nltk
from nltk.corpus import stopwords

def rank(verbose=False):
	tokenizer = RegexpTokenizer(r'\w+')
	ps = nltk.stem.PorterStemmer()
	weights = get_features(False)
	for filename in os.listdir("./dump-texts"):
		file = os.path.join("dump-texts",filename)
		url = filename[10:-4].replace('--','/')
		if verbose:
			print "RANKING " + url
		with open(file, 'r') as f:
			text = f.read().lower().decode('utf-8')
			text = re.sub(r'\d+', '', text)
			filtered_text = [w for w in tokenizer.tokenize(text) if w not in stopwords.words('english')]
			cur_tokens = [ps.stem(x) for x in filtered_text]
			score = 0
			for t in cur_tokens:
				if t in weights.keys():
					score += weights[t]
			score = score/len(cur_tokens)
			if verbose:
				print "SCORE = ", score


def main():
	rank(True)

if __name__ == '__main__':
	main()