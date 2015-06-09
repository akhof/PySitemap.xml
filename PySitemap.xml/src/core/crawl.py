#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import httplib, datetime, copy, robotparser
from lxml import html

def crawl(sitemap, defaultChangeFreq=None, useServersLastMod=True, defaultLastMod=None, defaultPriority=None):
    """
    sitemap                a Sitemap-instance to load data into
    defaultChangeFreq      the defaultChangeFreq
    useServersLastMod      use the serves lastMod?
    defaultLastMod         the lastMod to use if the server doesn't send a lastmod or useServersLastMod==False
        "now", "today", datetime.date, datetime.datetime
    defaultPriority        the defaultPriority
        None, 0.0..1.0, "auto" 
    """
    
    robots = None
    if sitemap.userobots:
        try:
            robots = robotparser.RobotFileParser(url=("https://" if sitemap.useHTTPS else "http://") + sitemap.domain + "/robots.txt")
            robots.read()
        except: print(u"Cannot read '{}/robots.txt'!".format(sitemap.domain))
    
    crawlingList = [sitemap.firstUrlToCrawl] #Elemente zu crawln
    crawledYet = []
    
    countLinks = {} #key=link value=linksTOcount
    
    while True:
        url = crawlingList[0]
        
        try:
            status, content, headers = download(sitemap, url)
            
            if status != 200: continue
            
            changefreq = defaultChangeFreq
            lastmod = None
            priority = None
            
            index, _, links = analyContent(sitemap, content)
            
            if not checkIsHtmlFromHeaders(headers) and sitemap.onlyHtml:
                continue
            if useServersLastMod:
                lastmod = readLastModFromHeaders(headers)
            if not useServersLastMod or (useServersLastMod and lastmod == None) and defaultLastMod != None:
                if defaultLastMod == "now":
                    lastmod = datetime.datetime.now()
                elif defaultLastMod == "today":
                    lastmod = datetime.date.today()
                elif type(defaultLastMod) in (datetime.date, datetime.datetime):
                    lastmod = defaultLastMod
                    
            if type(defaultPriority) in (int, float, long):
                priority = defaultPriority
            
            if index:
                sitemap.addUrl(url, changefreq, lastmod, priority)
            
            for link in links:
                if link not in countLinks: countLinks[link] = 1   
                else: countLinks[link] += 1
                    
                if link not in crawledYet:
                    if robots == None: allowed = True
                    else: allowed = robots.can_fetch("*", ("https://" if sitemap.useHTTPS else "http://") + sitemap.domain + link)
                    if allowed:
                        crawlingList.append(link)
                        crawledYet.append(link)
        except KeyboardInterrupt:
            raise
        except:
            continue
        finally:
            del(crawlingList[0])
            if len(crawlingList) == 0: break
    
    slash = False #ist die Url  /  vorhanden
    for url in sitemap.urls.keys():
        if url == "/": 
            slash = True
            break
    if slash:
        for url in sitemap.urls.keys():
            if url in ("/index.php", "/index.html"):
                sitemap.delUrl(url)
    
    
    if defaultPriority == "auto":
        list_linksto = []
        
        for link, count in copy.deepcopy(countLinks).iteritems():
            if link not in sitemap.urls.keys():
                del(countLinks[link])
            else:
                if count not in list_linksto:
                    list_linksto.append(count)
        
        linksto = {1.0:0, 0.9:0, 0.8:0, 0.7:0, 0.6:0, 0.5:0, 0.4:0, 0.3:0, 0.2:0}
        
        if len(list_linksto) > 0:
            if len(list_linksto) == 1:
                list_linksto *= 9
            elif len(list_linksto) == 2:
                list_linksto *= 4
                list_linksto.append((list_linksto[0]+list_linksto[1])//2)
            elif len(list_linksto) == 3:
                list_linksto *= 3
            elif len(list_linksto) == 4:
                list_linksto *= 2
                list_linksto.append((list_linksto[1]+list_linksto[2])//2)
            elif len(list_linksto) == 5:
                list_linksto *= 2
            elif len(list_linksto) == 6:
                list_linksto.append(list_linksto[3])
                for _ in range(2): list_linksto.append((list_linksto[2]+list_linksto[3])//2)
            elif len(list_linksto) == 7:
                for _ in range(2): list_linksto.append(list_linksto[4])
            elif len(list_linksto) == 8:
                list_linksto.append((list_linksto[3]+list_linksto[4])//2)
            list_linksto.sort()
        
        
            linksto[10] = list_linksto[-1]
            linksto[9] = list_linksto[len(list_linksto) - (len(list_linksto)//5)]
            linksto[8] = list_linksto[len(list_linksto) - (len(list_linksto)//4)]
            linksto[7] = list_linksto[len(list_linksto) - (len(list_linksto)//3)]
            linksto[6] = list_linksto[len(list_linksto)//2]
            linksto[5] = list_linksto[len(list_linksto)//3]
            linksto[4] = list_linksto[len(list_linksto)//4]
            linksto[3] = list_linksto[len(list_linksto)//5]
            linksto[2] = list_linksto[0]
            
            for url in sitemap.urls.values():
                if (not slash and url.loc in ("/index.html", "(index.php")) or (slash and url.loc == "/"):
                    i = 10
                else:
                    i = 2
                    while True:
                        if countLinks[url.loc] > linksto[i]:
                            if i == 10: break
                            else: i += 1
                        elif countLinks[url.loc] < linksto[i]:
                            if i != 2: i -= 1
                            break
                        else:
                            break
                url.priority = i/10.0
    
    for url in sitemap.urls.values():
        url.loc = "https://" if sitemap.useHTTPS else "http://" + sitemap.domain + url.loc
    

def analyContent(sitemap, content):
    parser = html.HTMLParser()
    tree = html.document_fromstring(content, parser)
    
    hrefs = []
    robots = "index, follow"
    def analyChilds(node, ebene=0):
        for child in node.getchildren():
            try:
                if child.tag.lower() == "meta" and "name" in child.attrib and "content" in child.attrib:
                    if child.attrib["name"] == "meta":
                        robots = child.attrib["content"]
                elif child.tag.lower() == "a" and "href" in child.attrib:
                    hrefs.append(child.attrib["href"])
            except AttributeError:
                pass
            finally:
                analyChilds(child, ebene+1)
    analyChilds(tree)

    index = "index" in robots
    follow = "follow" in robots
    
    if not follow: return index, follow, []
    
    newLinks = {} #dict, damit nicht mehrere gleiche links vorhanden
    for href in hrefs:
        if href[0] == "#": continue
        else: href = href.split("#")[0]
        if sitemap.ignoreUrlArguments: href = href.split("?")[0]
        
        if href.replace("https://", "").replace("http://", "").replace("/", "") == sitemap.domain:
            newLinks["/"] = None
        elif ("http://" in href or "https://" in href or "mailto:" in href) or href[0] != "/":
            continue
        else:
            newLinks[href] = None
    
    return index, follow, newLinks.keys()

def checkIsHtmlFromHeaders(headers):
    for header in headers:
        if header[0].lower() == "content-type":
            try: return "text/html" in header[1]
            except: pass
    return False
def readLastModFromHeaders(headers):
    for header in headers:
        if header[0].lower() == "last-modified":
            try: return datetime.datetime.strptime(header[1], "%a, %d %b %Y %H:%M:%S GMT")
            except: pass


def download(sitemap, url):
    if sitemap.showDownloadDetails: print("Download: \t{}{}".format(sitemap.domain.replace("/",""), url))
    
    if sitemap.useHTTPS:    cls = httplib.HTTPSConnection
    else:                   cls = httplib.HTTPConnection
    
    con = cls(sitemap.domain)
    con.request("GET", url)
    r = con.getresponse()
    
    status = r.status
    content = r.read()
    headers = r.getheaders()
    
    con.close()
    
    return status, content, headers