from bs4 import BeautifulSoup
import urllib2
import html2text
import pprint
import os
import shutil
import requests

def save_page_text(url):
    try:
        page_response = requests.get(url, timeout=5, headers=headers)
    except:
        print "ERROR is saving text of url: ", url
        return
    soup = BeautifulSoup(page_response.content, "html.parser")
    text = soup.findAll(['p', 'a', 'h1', 'h2'], text=True)
    if (text is not None):
        # raw_list = text.splitlines()
        new_list = []
        for line in text:
            line = line.encode('utf-8').strip()
            if line != '':
                line = line + '\n'
                new_list.append(line)
        clean_text = "".join(new_list)
        file_name = url.replace('/','')
        f = open("dump-texts/" + file_name + '.txt', "w")
        f.write(clean_text)
        f.close()
    else:
        print "ERROR in html to text parser for url: ", url
        return

# def get_next_target(page):
#     start_link = page.find('<a href=')
#     if start_link == -1:
#         return None,0
#     start_quote = page.find('"',start_link)
#     end_quote = page.find('"',start_quote+1)
#     url = page[start_quote+1:end_quote]
#     return url,end_quote

# def print_all_links(page):
#     while True:
#         url, endpos=get_next_target(page)
#         if url:
#             print url
#             page=page[endpos:]
#         else:
#             break

def get_page(url):
    try:                                
        content = urllib2.urlopen(url).read()
        return content
    except:
        print "ERROR GETTING THE PAGE: ", url
        return None

def get_all_links(page_url):
    links=[]
    page_response = requests.get(url, timeout=5, headers=headers)
    soup = BeautifulSoup(page_response.content, "html.parser")
    # print("*********** Printing links for Page: ",page_url)        
    for link in soup.find_all('a', href=True):
        link = unicode(link.get('href'))
        # if link.find("http://www.")== -1 or link.find("http://") == -1:
        #     link = page_url + '/' + link
        # print(link)
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
# page_response = requests.get(url, timeout=5, headers=headers)
# soup = BeautifulSoup(page_response.content, "html.parser")
# data = soup.findAll(text=True)
graph = crawl_web(url)
# pprint.pprint(graph)
