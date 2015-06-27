#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import xml.etree.cElementTree as ET
import xml.dom.minidom as md
from datetime import datetime, date

def createXml(sitemap, useChangeFreq=False, useLastModification=False, usePriority=False, dateformat="%Y-%m-%d", datetimeformat="%Y-%m-%dT%H:%M:%S"):
    urlset = ET.Element("urlset")
    urlset.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")
    urlset.append( ET.Comment("created with PySitemap.xml at {}".format(datetime.today().strftime(datetimeformat))))
    urlset.append( ET.Comment("pages in sitemap: {} ".format(len(sitemap.urls.keys()))) )
    
    for url in sitemap.urls.values():
        xmlUrl = ET.SubElement(urlset, "url")
        
        ET.SubElement(xmlUrl, "loc").text = url.loc
        
        if usePriority and url.priority != None:
            ET.SubElement(xmlUrl, "priority").text = str(float(url.priority))
        
        if useChangeFreq and url.changefreq != None:
            ET.SubElement(xmlUrl, "changefreq").text = url.changefreq.lower()
        
        
        if useLastModification and url.lastmod != None:
            lmod = url.lastmod
            
            if type(lmod) == str:
                txt = lmod
            elif type(lmod) == date:
                txt = lmod.strftime(dateformat)
            elif type(lmod) == datetime:
                txt = lmod.strftime(datetimeformat)
            else:
                lmod = None

            if lmod != None:
                ET.SubElement(xmlUrl, "lastmod").text = txt
    
    xml = ET.tostring(urlset, "utf-8")
    return md.parseString(xml).toprettyxml()