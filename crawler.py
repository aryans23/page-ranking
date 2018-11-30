from bs4 import BeautifulSoup
import pprint
import os
import shutil
import requests
import re

def save_page_text(url):
    try:
        page_response = requests.get(url, timeout=5, headers=headers)
    except:
        print "ERROR in saving text of url: ", url
        return
    soup = BeautifulSoup(page_response.content, "html.parser")
    for node in soup.findAll(['p', 'a', 'h1', 'h2']):
        line = ''.join(node.findAll(text=True))
        line = line.strip()
        line = line.encode('utf-8')
        file_name = url.replace('/','')
        f = open("dump-texts/" + file_name + '.txt', "a+")
        f.write(line)
        f.close()

def get_all_links(page_url):
    links=[]
    page_response = requests.get(url, timeout=5, headers=headers)
    soup = BeautifulSoup(page_response.content, "html.parser")
    # print("*********** Printing links for Page: ",page_url)        
    for link in soup.find_all('a', href=True):
        link = unicode(link.get('href'))
        if not re.match(r'^http', link):
            link = page_url + '/' + link
        links.append(link)
    # print("*********** End Printing links")
    return links

def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)

def crawl_web(seed_url):
    tocrawl = [seed_url]
    crawled = set()
    graph = {}
    while (tocrawl and len(crawled) <= pageslimit):
        f_crawled = open("html-crawled.txt", "a+")
        page_url = tocrawl[0]
        tocrawl = tocrawl[1:]
        if page_url not in crawled:
            outlinks = get_all_links(page_url)
            crawled.add(page_url)
            f_crawled.write(page_url + "\n")
            f_crawled.close()
            if (len(outlinks) == 0):
                continue
            union(tocrawl, outlinks)
            graph[page_url] = outlinks
            save_page_text(page_url)
        print "************* Graph size =",len(graph)
    return graph

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
# url = "https://www.amazon.com/"
url = "http://courses.cse.tamu.edu/caverlee/csce670/index.html"
pageslimit = 20
if os.path.exists("html-crawled.txt"):
    os.remove("html-crawled.txt")
if os.path.exists("dump-texts"):
    shutil.rmtree("./dump-texts")
os.makedirs("dump-texts")
graph = crawl_web(url)
# pprint.pprint(graph)
