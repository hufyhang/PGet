#!/usr/bin/python

# A widget app written in Python to download resources from Internet
# Author: Feifei Hang
# Last Update: Fri 31-05-2013 04:18 pm

import urllib2
import urlparse
import sys
import json

CHUNK_SIZE = 8192

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
        totalLength = int(u.info().getheader('Content-Length').strip())
        if filename == None:
            filename = getFileName(url)
        print 'Downloading : ' + filename
        localfile = open(filename, 'w')
        buffer = ''
        while 1:
            buffer += u.read(CHUNK_SIZE)
            readLength = len(buffer)
            percent = float(readLength) / totalLength
            percent = round(percent * 100, 2)
            barsNumber = percent // 10
            barsNumber = int(barsNumber)
            bars = '|'
            if barsNumber != 10:
                for index in range(0, barsNumber - 1):
                    bars += '='
                bars += '>'
                for index in range(barsNumber, 10):
                    bars += ' '
                bars += '|'
            else:
                bars = '|==========|'
            sys.stdout.write("Downloaded %d of %d bytes (%0.2f%%) %s \r" %(readLength, totalLength, percent, bars))
            if percent == 100:
                break

        localfile.write(buffer)
        localfile.close()
        sys.stdout.write('\n')
    except:
        print 'Oops! Cannot download ', url

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
        print 'Try to download from list: ', ls
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


