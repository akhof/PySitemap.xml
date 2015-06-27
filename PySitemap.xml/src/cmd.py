#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import argparse, time, sys
from PySitemap import *

def run():
    print("PySitemap.xml {}\n".format(VERSION))
    
    parser = argparse.ArgumentParser(prog="PySitemap.xml")
    
    parser.add_argument("Domain",                                                                               help="Domain to create a sitemap")
    parser.add_argument("-f",       "--firstUrl",                                   default="/",                help="First URL to call (default:'/')")
    parser.add_argument("-t",       "--https",              action="store_true",    default=False,              help="Use HTTPS and not HTTP")
    parser.add_argument("-i",       "--ignoreArgs",         action="store_true",    default=False,              help="Ignore HTTP-Arguments (e.g.: '/index.php?arg1=...&arg2=...')")
    parser.add_argument("-o",       "--onlyHtml",           action="store_true",    default=False,              help="Only add Pages with HTML-content to sitemap")
    parser.add_argument("-r",       "--userobots",          action="store_true",    default=False,              help="Read the robots.txt and only add allowed pages to sitemap")
    parser.add_argument("-c",       "--useChangeFreq",      action="store_true",    default=False,              help="Add a  ChangeFreq  to sitemap")
    parser.add_argument("-l",       "--useLastMod",         action="store_true",    default=False,              help="Add a  LastMod  to sitemap")
    parser.add_argument("-p",       "--usePriority",        action="store_true",    default=False,              help="Add a  Priority  to sitemap")
    parser.add_argument(            "--defaultChangeFreq",                          default=None,               help="Default  ChangeFreq")
    parser.add_argument(            "--defaultLastMod",                             default=None,               help="Default  LastMod")
    parser.add_argument(            "--defaultPriority",                            default=None,   type=float, help="Default  Priority")
    parser.add_argument("-a",       "--autoPriority",       action="store_true",    default=False,              help="Auto calculate the  Priority")
    parser.add_argument("-u",       "--useServesLastMod",   action="store_true",    default=False,              help="Use the serves's lastMod")
    parser.add_argument("-s",       "--save",                                       default=None,               help="Save the sitemap in a file")
    parser.add_argument(            "--console",            action="store_true",    default=False,              help="Print the sitemap in a console")
    parser.add_argument(            "--details",            action="store_true",    default=False,              help="Show Download-Details")
    
    args = parser.parse_args()
    
    if args.save == None and not args.console:
        print("WARNING: You don't print or save generated sitemap! Press STRG+C to cancel...\n")
        time.sleep(2)
    
    sitemap = Sitemap(
                      domain              = args.Domain,
                      useHTTPS            = args.https,
                      ignoreUrlArguments  = args.ignoreArgs,
                      onlyHtml            = args.onlyHtml,
                      firstUrlToCrawl     = args.firstUrl,
                      showDownloadDetails = args.details,
                      userobots = args.userobots
                    )
    
    print("Start generating XML-Sitemap...\n")
    starttime = time.time()
    
    
    crawl(
           sitemap,
           args.defaultChangeFreq,
           args.useServesLastMod,
           args.defaultLastMod,
           "auto" if args.autoPriority else args.defaultPriority
          )
    xml = createXml(
                      sitemap,
                      args.useChangeFreq,
                      args.useLastMod,
                      args.usePriority
                    )
    
    print("Finished creating sitemap in {}s".format(round(time.time()-starttime, 5)))
    
    if args.save != None:
        try:
            f = open(args.save, "w")
            f.write(xml)
            print(u"Saved sitemap at '{}'".format(args.save))
        except Exception as FM:
            print(u"Cannot save sitemap at '{}':\n\t{}".format(args.save, FM))
        finally:
            try: f.close()
            except: pass
    if args.console:
        print("\n{0}  GENERATED XML-SITEMAP  {0}".format(15*'*'))
        print(xml)

if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print("\n\nAbort...")
        sys.exit(1)