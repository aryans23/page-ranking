from features import get_features
import os
from nltk.tokenize import RegexpTokenizer
import re
import nltk
from nltk.corpus import stopwords
from Queue import PriorityQueue

class Ranker():
	"""docstring for Ranker"""
	def __init__(self,verbose=False):
		self.verbose = verbose
		self.ranks = []
		
	def _calculate_url_bonus(self,url):
		bonus = 0
		if "service" in url:
			bonus += 0.5
		if "buy" in url:
			bonus += 0.5
		if "product" in url:
			bonus += 0.5
		if "price" in url:
			bonus += 0.5
		return bonus

	def _dump_ranks(self,ranks):
		while not ranks.empty():
			next_item = ranks.get()
			self.ranks.append(next_item)

	def rank(self):
		tokenizer = RegexpTokenizer(r'\w+')
		ps = nltk.stem.PorterStemmer()
		weights = get_features(self.verbose)
		ranks = PriorityQueue()
		for filename in os.listdir("./dump-texts"):
			file = os.path.join("dump-texts",filename)
			url = filename[10:-4].replace('--','/')
			if self.verbose:
				print "\nSCORING " + url
			with open(file, 'r') as f:
				text = f.read().lower().decode('utf-8')
				text = re.sub(r'\d+', '', text)
				filtered_text = [w for w in tokenizer.tokenize(text) if w not in stopwords.words('english')]
				cur_tokens = [ps.stem(x) for x in filtered_text]
				score = 0
				text_bonus = 0
				for t in cur_tokens:
					if 'buy' in t:
						text_bonus += 3
					elif 'price' in t:
						text_bonus += 3
					if t in weights.keys():
						score += weights[t]
					score += text_bonus
				score = score/len(cur_tokens)
				score += self._calculate_url_bonus(url)
				if self.verbose:
					print "SCORE = " + str(score) + "\n"
				ranks.put((-1*score, url))
		self._dump_ranks(ranks)
		print "************* Ranks computed!"

	def print_ranks(self):
		print "************* Printing Ranks...\n"
		print "----------------------------------------------------------------"
		i = 1
		for tup in self.ranks:
			print str(i) + ". " + tup[1]
			i += 1
		print "----------------------------------------------------------------"
		print "\n************* Printed Ranks!"

def main():
	ranker = Ranker(verbose=False)
	ranker.rank()
	ranker.print_ranks()

if __name__ == '__main__':
	main()