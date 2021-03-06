#!/usr/bin/python

# A widget app written in Python to download resources from Internet
# Author: Feifei Hang

import urllib2
import urlparse
import sys
import json
import os

LAST_MODIFICATION = 'Fri 31-05-2013 09:47 pm'
UPDATE_JSON = 'http://feifeihang.info/app/pget/update.json'
CHUNK_SIZE = 8192

PGET_PATH = os.path.abspath(os.path.dirname(__file__)) + '/'

USAGE = '''Usage: python pget.py [option] [List 1] [List 2] ... [List N]
    -l: Download from JSON list.
    -u: Update PGet.
    -v: Show the latest modification of PGet.
'''

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
        dirname = os.path.dirname(filename)
        if dirname != '': #if dirname equals to '', then it is pointing to the current directory.
            if not os.path.exists(dirname):
                os.makedirs(dirname)
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
                bars = '|===Done===|'
            sys.stdout.write("Downloaded %d of %d bytes (%0.2f%%) %s \r" %(readLength, totalLength, percent, bars))
            if percent == 100:
                break

        localfile.write(buffer)
        localfile.close()
        sys.stdout.write('\n')
    except:
        print 'Oops! Cannot download ', url

def downloadFromJSON(lf, destDir=''):
    jsonData = json.load(lf)
    for item in jsonData:
        filename = item
        url = jsonData[item]
        downloadFile(url, destDir + filename)
    
if len(sys.argv) == 1:
    print USAGE
    sys.exit(0)

if sys.argv[1] == '-l':
    if len(sys.argv) == 2:
        print USAGE
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

elif sys.argv[1] == '-u':
    print 'Updating sequence started...'
    lf = urllib2.urlopen(urllib2.Request(UPDATE_JSON, headers=hdr))
    downloadFromJSON(lf, PGET_PATH)
elif sys.argv[1] == '-v':
    print 'PGet Last Modified: ', LAST_MODIFICATION
else:
    for index in range(1, len(sys.argv)):
        url = sys.argv[index]
        downloadFile(url)
