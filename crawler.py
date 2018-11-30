from bs4 import BeautifulSoup
import urllib2
import html2text
import pprint
import os
import shutil

def save_page_text(page):
    html = get_page(page)
    if (html is not None and page[-4:] is not ".pdf"):
        try:
            text = html2text.html2text(html)
        except:
            print "ERROR in html to text parser for page: ", page
            return
        raw_list = text.splitlines()
        new_list = []
        for line in raw_list:
            line = line.encode('utf-8').strip()
            if line != '':
                line = line + '\n'
                new_list.append(line)
        clean_text = "".join(new_list)
        file_name = page.replace('/','')
        f = open("dump-texts/" + file_name + '.txt', "w")
        f.write(clean_text)
        f.close()

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
        return

def get_all_links(page):
    links=[]
    # print("*********** Printing links for Page: ",page)        
    for link in soup.find_all('a', href=True):
        link = unicode(link.get('href'))
        # if link.find("http://www.")== -1 or link.find("http://") == -1:
        #     link = page + '/' + link
        # print(link)
        links.append(link)
    # print("*********** End Printing links")
    return links

def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)

def crawl_web(seed):
    tocrawl = [seed]
    crawled = set()
    graph = {}
    while (tocrawl and len(crawled) <= pageslimit):
        f_crawled = open("crawled.txt","a+")
        page = tocrawl[0]
        tocrawl = tocrawl[1:]
        if page not in crawled:
            outlinks = get_all_links(page)
            crawled.add(page)
            f_crawled.write(page+"\n")
            f_crawled.close()
            if (len(outlinks) == 0):
                continue
            union(tocrawl, outlinks)
            graph[page] = outlinks
            save_page_text(page)
        print("************* Graph size = ",len(graph))
    return graph

page = "http://courses.cse.tamu.edu/caverlee/csce670/schedule.html"
pageslimit = 20
if os.path.exists("dump-texts"):
    shutil.rmtree("./dump-texts")
os.makedirs("dump-texts")
content = get_page(page)
soup = BeautifulSoup(content, 'html.parser')
graph = crawl_web(page)
# pprint.pprint(graph)
