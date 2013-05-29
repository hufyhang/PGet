#!/usr/bin/python

# A widget app written in Python to download resources from Internet
# Author: Feifei Hang
# Last Update: Tue 28-05-2013 08:44 pm

import urllib2
import urlparse
import sys
import json

PROTOCOLS = ['HTTP', 'HTTPS', 'FTP']

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

def getFileName(url):
    return urlparse.urlsplit(url).path.split('/')[-1]

def getHttpProtocol(url):
    return url.split(':')[0]

def downloadFile(url, filename=None):
    try:
        req = urllib2.Request(url, headers=hdr)
        u = urllib2.urlopen(req)
        if filename == None:
            filename = getFileName(url)
        print 'Downloading : ' + filename + '. Please wait...'
        localfile = open(filename, 'w')
        localfile.write(u.read())
        localfile.close()
        print 'Done.'
    except:
        print 'Oops! Cannot download ',  url

def downloadFromJSON(lf):
    jsonData = json.load(lf)
    for item in jsonData:
        filename = item
        url = jsonData[item]
        downloadFile(url, filename)
    
if len(sys.argv) == 1:
    print 'Usage: python pget.py (-l) [URL 1] [URL 2] ... [URL N]'
    print '-l -- to download from JSON list'
    sys.exit(0)

if sys.argv[1] != '-l':
    for index in range(1, len(sys.argv)):
        url = sys.argv[index]
        downloadFile(url)
else:
    if len(sys.argv) == 2:
        print 'Usage: python pget.py (-l) [List 1] [List 2] ... [List N]'
        sys.exit(0)

    for index in range(2, len(sys.argv)):
        ls = sys.argv[index]
        protocol = getHttpProtocol(ls)
        if protocol.upper() in PROTOCOLS:
            try:
                lf = urllib2.urlopen(urllib2.Request(ls, headers=hdr))
                downloadFromJSON(lf)
            except:
                print 'Oops! JSON error in ', ls
        else:
            try:
                lf = open(ls, 'r')
                downloadFromJSON(lf)
                lf.close()
            except:
                print 'Oops! Cannot open ', ls


