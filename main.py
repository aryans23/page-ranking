from crawler import Crawler
from rank import Ranker

def main():
	url = "https://www.microsoft.com/"
	# url = "https://azure.microsoft.com/en-us/"
	# url = "https://www.nvidia.com/"
	# url = "https://www.apple.com/"
	# url = "http://courses.cse.tamu.edu/caverlee/csce670/index.html"

	crawler = Crawler(limit=50,verbose=False)
	crawler.crawl_web(url)
	ranker = Ranker(verbose=False)
	ranker.rank()
	ranker.print_ranks()

if __name__ == '__main__':
	main()