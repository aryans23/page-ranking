from bs4 import BeautifulSoup
import pprint
import os
import shutil
import requests
import re
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}

class Crawler():
    """docstring for Crawler"""
    def __init__(self,limit=50,verbose=False):
        self.pageslimit = limit
        self.verbose = verbose
        self.graph = {}
        self.count_links = {}
        if os.path.exists("html-crawled.txt"):
            os.remove("html-crawled.txt")
        if os.path.exists("dump-texts"):
            shutil.rmtree("./dump-texts")
        os.makedirs("dump-texts")

    def _save_page_text(self,url):
        try:
            page_response = requests.get(url, timeout=5)
            # page_response = requests.get(url, timeout=5, headers=headers)
        except:
            print "ERROR in saving text of url: ", url
            return
        soup = BeautifulSoup(page_response.content, "html.parser")
        for node in soup.findAll(['p', 'a', 'h1', 'h2']):
            line = ''.join(node.findAll(text=True))
            line = line.strip()
            line = line.encode('utf-8')
            file_name = url.replace('/','--')
            f = open("dump-texts/processed-" + file_name + '.txt', "a+")
            f.write(line)
            f.close()

    def _get_all_links(self,page_url):
        links = []
        count = 0
        try:
            page_response = requests.get(page_url, timeout=5)
        except Exception as e:
            raise e
        # page_response = requests.get(url, timeout=5, headers=headers)
        soup = BeautifulSoup(page_response.content, "html.parser")
        # print("*********** Printing links for Page: ",page_url)        
        for link in soup.find_all('a', href=True):
            link = unicode(link.get('href'))
            # print link
            if not re.match(r'^http', link):
                link = page_url + '/' + link
            links.append(link)
            count += 1
        # print("*********** End Printing links, count = ", count)
        return links, count

    def _union(self,p,q):
        for e in q:
            if e not in p:
                p.append(e)

    def crawl_web(self,seed_url):
        print "************* Crawling webpages..."
        tocrawl = [seed_url]
        crawled = set()
        while (tocrawl and len(crawled) <= self.pageslimit):
            f_crawled = open("html-crawled.txt", "a+")
            page_url = tocrawl[0]
            tocrawl = tocrawl[1:]
            if page_url not in crawled:
                outlinks, num_links = self._get_all_links(page_url)
                crawled.add(page_url)
                f_crawled.write(page_url + "\n")
                f_crawled.close()
                if (len(outlinks) == 0):
                    continue
                self._union(tocrawl, outlinks)
                self.graph[page_url] = outlinks
                self.count_links[page_url] = num_links
                self._save_page_text(page_url)
            if self.verbose:
                print "************* Graph size =",len(self.graph)
        print "************* All pages crawled!"
        return self.graph, self.count_links



