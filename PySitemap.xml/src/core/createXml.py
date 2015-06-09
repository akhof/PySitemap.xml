#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import xml.etree.cElementTree as ET
import xml.dom.minidom as md
from datetime import datetime, date

def createXml(sitemap, useChangeFreq=False, useLastModification=False, usePriority=False):
    urlset = ET.Element("urlset")
    urlset.append( ET.Comment(" Created with PySitemap ") )
    urlset.append( ET.Comment(" {} ".format(datetime.today().strftime("%Y-%m-%d %H:%M:%S"))) )
    c=0 
    
    for url in sitemap.urls.values():
        c+=1
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
                txt = lmod.strftime("%Y-%m-%d")
            elif type(lmod) == datetime:
                txt = lmod.strftime("%Y-%m-%dT%H:%M:%S")
            else:
                continue

            ET.SubElement(xmlUrl, "lastmod").text = txt
    
    xml = md.parseString(ET.tostring(urlset, "utf-8")).toprettyxml()
    xml = xml.replace("<urlset", """<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd\"""")
    print c
    return xml