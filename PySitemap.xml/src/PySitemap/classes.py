#!/usr/bin/env python
# -*- coding: UTF-8 -*-

class UrlAlreadyInSitemap(Exception): pass
class UrlNotInSitemap(Exception): pass

class Url():
    def __init__(self, loc, changefreq=None, lastmod=None, priority=None):
        self.loc = loc
        self.changefreq = changefreq
        self.lastmod = lastmod
        self.priority = priority

class Sitemap():
    def __init__(self, title="", domain="", useHTTPS=False, ignoreUrlArguments=True, onlyHtml=True, firstUrlToCrawl="/", showDownloadDetails=False, userobots=False):
        self.title = title
        self.domain = domain.split("http://")[-1].split("https://")[-1]
        self.useHTTPS = useHTTPS
        self.ignoreUrlArguments = ignoreUrlArguments
        self.onlyHtml = onlyHtml
        self.firstUrlToCrawl = firstUrlToCrawl
        self.showDownloadDetails = showDownloadDetails
        self.userobots = userobots
        
        while self.domain[-1] == "/": self.domain = self.domain[:-1] # google.com/  ->  google.com
        
        self.urls = {}
    
    def addUrl(self, loc, changefreq=None, lastmod=None, priority=None):
        if not self.isUrlInSitepam(loc):
            self.urls[loc] = Url(loc, changefreq, lastmod, priority)
        else:
            raise UrlAlreadyInSitemap()
    
    def delUrl(self, loc):
        if self.isUrlInSitepam(loc):
            del(self.urls[loc])
        else:
            raise UrlNotInSitemap()
    
    def editUrl(self, loc, changefreq=None, lastmod=None, priority=None):
        if self.isUrlInSitepam(loc):
            self.urls[loc].changefreq = changefreq
            self.urls[loc].lastmod = lastmod
            self.urls[loc].priority = priority
        else:
            raise UrlNotInSitemap()
                
    def isUrlInSitepam(self, loc):
        return loc in self.urls.keys()
