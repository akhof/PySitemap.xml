# PySitemap.xml
PySitemap.xml is a tool to create xml-sitemaps with python.  NOT TESTED FULL!!! v.01.1.BETA1!!!

## Requirements
* Python 2
* modules: httplib, lxml, argparse
 
## Usage
You can run the /src/cmd.py in console to create a sitemap or you can import the module /src/core from your python-code:

### Import as module
    from core import *
    s = Sitemap(domain="yourdomain.com")
    crawl(s, defaultChangeFreq="monthly", defaultPriority=0.5)
    xml = createXml(s)
    
    print xml
    

### Usage in console
    usage: PySitemap.xml  v.0.1.beta1 [-h] [-f FIRSTURL] [-t] [-i] [-o] [-r] [-c] [-l]                                                                                                                                                    
				      [-p] [--defaultChangeFreq DEFAULTCHANGEFREQ]                                                                                                                                                                                                 
				      [--defaultLastMod DEFAULTLASTMOD]                                                                                                                                                                                                            
				      [--defaultPriority DEFAULTPRIORITY] [-a]                                                                                                                                                                                                     
				      [-u] [-s SAVE] [--console] [--details]                                                                                                                                                                                                       
				      Domain                                                                                                                                                                                                                                       
																																
    positional arguments:                                                                                                                                                                                                                                                          
      Domain                Domain to create a sitemap                                                                                                                                                                                                                             
																																
    optional arguments:                                                                                                                                                                                                                                                            
      -h, --help            show this help message and exit                                                                                                                                                                                                                        
      -f FIRSTURL, --firstUrl FIRSTURL                                                                                                                                                                                                                                             
			    First URL to call (default:'/')                                                                                                                                                                                                                        
      -t, --https           Use HTTPS and not HTTP                                                                                                                                                                                                                                 
      -i, --ignoreArgs      Ignore HTTP-Arguments (e.g.:                                                                                                                                                                                                                           
			    '/index.php?arg1=...&arg2=...')                                                                                                                                                                                                                        
      -o, --onlyHtml        Only add Pages with HTML-content to sitemap                                                                                                                                                                                                            
      -r, --userobots       Read the robots.txt and only add allowed pages to sitemap
      -c, --useChangeFreq   Add a ChangeFreq to sitemap                                                                                                                                                                                                                            
      -l, --useLastMod      Add a LastMod to sitemap                                                                                                                                                                                                                               
      -p, --usePriority     Add a Priority to sitemap                                                                                                                                                                                                                              
      --defaultChangeFreq DEFAULTCHANGEFREQ
			    Default ChangeFreq
      --defaultLastMod DEFAULTLASTMOD
			    Default LastMod
      --defaultPriority DEFAULTPRIORITY
			    Default Priority
      -a, --autoPriority    Auto calculate the Priority
      -u, --useServesLastMod
			    Use the serves's lastMod
      -s SAVE, --save SAVE  Save the sitemap in a file
      --console             Print the sitemap in a console
      --details             Show Download-Details

## Links
* [PySitemap.xml - Website](http://www.arnehannappel.de/index.php/projekte/python-module/pysitemap-xml)
