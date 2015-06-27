#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from classes import *
from createXml import createXml
from crawl import crawl

VERSION = "0.1.1"
USAGE = """
USAGE
=====

Classes:
  * Url                            an  Url-instance  describes one page in a sitemap
  * Sitemap                        a  Sitemap-instance  contains the sitemap's information
Exeptions:
  * UrlAlreadyInSitemap            this exception is raised if you try to add an Url to Sitemap, which is already in sitemap
  * UrlNotInSitemap                this exception is raised if you try to edit/del an Url from sitemap, which doesn't contains this
Functions:
  * crawl                          this function starts to crawl pages and add this into a sitemap
  * createXml                      this function generates a Xml-sitemap from a Sitemap-instance
Strings:
  * VERSION                        the module's version
  * USAGE                          this usage-info


Url
    + __init__(self, loc, changefreq=None, lastmod=None, priority=None)
    - loc                          e.g.:            "/index.php/example"
    - changefreq                   one of this:     None, "always", "hourly", "daily", "weekly", "monthly", "yearly", "never"
    - lastmod                      None or a datetime.datetime- or a datetime.date-instance
    - priority                     None or a float 0.0..1.0
Sitemap
    + __init__(self, title="", domain="", useHTTPS=False, ignoreUrlArguments=True, onlyHtml=True, firstUrlToCrawl="/", showDownloadDetails=False, userobots=False):
    - title                        a sitemap's title
    - domain                       the sitemap's domain (e.g: "http://example.com")
    - useHTTPS                     use https and not http
    - ignoreUrlArguments           ignore Url-Arguments (e.g. "http://example.com?id=123&name=456")
    - onlyHtml                     add only sites with HTML-content
    - firstUrlToCrawl              set the first Url to crawl (normaly: "/")
    - showDownloadDetails          write download-Details to sys.stdout
    - userobots                    use robots and only add pages, which are allowed in robots.txt
    - urls                         a dict with all Urls  (key=loc  value=Url-instance)
    + addUrl(self, loc, changefreq=None, lastmod=None, priority=None)
        :return None
        :exception UrlAlreadyInSitemap
    + delUrl(self, loc)
        :return None
        :exception UrlNotInSitemap
    + editUrl(self, loc, changefreq=None, lastmod=None, priority=None)
        :return None
        :raise UrlNotInSitemap
    + isUrlInSitepam(self, loc)
        :return bool

    
+ crawl(sitemap, defaultChangeFreq=None, useServersLastMod=True, defaultLastMod=None, defaultPriority=None)
    :parameters
            sitemap                a Sitemap-instance to load data into
            defaultChangeFreq      one of this:     None, "always", "hourly", "daily", "weekly", "monthly", "yearly", "never"
            useServersLastMod      use the serves lastMod?
            defaultLastMod         the lastMod to use if the server doesn't send a lastmod or useServersLastMod==False
                                   one of this:    None, "now", "today", datetime.date, datetime.datetime
            defaultPriority        one of this:    None, 0.0..1.0
    :return None
+ createXml(sitemap, useChangeFreq=False, useLastModification=False, usePriority=False, dateformat="%Y-%m-%d", datetimeformat="%Y-%m-%dT%H:%M:%S")
    :parameters
            sitemap                a Sitemap-instance to load data into
            useChangeFreq          add the useChangeFreq to sitemap
            useLastModification    add the useLastModification to sitemap
            usePriority            add the usePriority to sitemap
            dateformat             the default date-format        ("%Y-%m-%d")
            datetimeformat         the default datetime-format    ("%Y-%m-%dT%H:%M:%S")
    :return str
"""