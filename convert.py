#!/usr/bin/env python

# -*- coding: utf-8-*-  

import getopt
import time
import re
import os,sys
reload(sys)
sys.setdefaultencoding('utf-8')
import random
from utils import Utils
from bs4 import BeautifulSoup
import requests

utils = Utils()

source = ''
prefix = 'convert'

keyword_min_number = 3
keyword_max_number = 7
custom_html_tag = 'a'
custom_filter = ''
custom_contain = ''
start = 0
end = 1000
line_id = 0
delete_from_char = ''

def printLine(line, link=''):
    #line_id = random.randrange(10, 100, 2)
    if link != '' and line.startswith('http') == False:
        link = source[0 : source.find('com') + 3] + link
    if delete_from_char != '' and line.find(delete_from_char) != -1: 
        line = line[0 : line.find(delete_from_char)].strip()
    print prefix + "-" + str(line_id) + " |"  + line.strip() + " | " + link + " |"


def convert(source):
    global start, line_id
    if source.startswith('http') or source.endswith('html'):
       html_content = ''
       if source.startswith('http'):
           user_agent = {'User-agent': 'Mozilla/5.0'}
           r = requests.get(source, headers = user_agent) 
           html_content = r.text
       elif source.endswith('html'):
           f = open(source)
           html_content = ''.join(f.readlines())
       for atag in custom_html_tag.strip().split(' '):
           soup = BeautifulSoup(html_content)
           for tag in soup.find_all(atag):
               line = utils.removeDoubleSpace(tag.text.strip().replace('\n', ' '))
               if keyword_min_number > keyword_max_number:
                  return
               split_list = line.split(' ')
               #print split_list  
               #print str(len(split_list)) + ' ' + str(keyword_min_number) + ' ' + str(keyword_max_number)
               if len(split_list) >= keyword_min_number and len(split_list) <= keyword_max_number:
                   if custom_filter != '':
                       filters = custom_filter.split(' ')
                       for ft in filters:
                           if line.find(ft) != -1:
                               line = ''
                               break
                   if line_id > end:
                       return     
                   if custom_contain != '':
                       custom_contain_split = custom_contain.split(' ')
                       skip = False
                       for c in custom_contain_split:
                           if c != '' and line.find(c) != -1:
                               skip = False
                               break
                           else:
                               skip = True
                       if skip: 
                           continue
                   if line != '':
                       line_id += 1
                   if line != '' and line_id >= start and line_id <= end:
                       if tag.attrs.has_key("href"):
                           printLine(line, tag['href'])
                       elif tag.a != None and tag.a.attrs.has_key("href"):
                            printLine(line, tag.a['href'])
                       else:
                            printLine(line)
    else:
        f = open(source)
        lines = f.readlines()
        data = ''.join(lines)
        data = utils.clearHtmlTag(data)
    
        for line in data.split('\n'):
            printLine(line)

def main(argv):
    global source, keyword_min_number, keyword_max_number, custom_html_tag, custom_filter
    global start, end, custom_contain, delete_from_char
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'i:u:n:m:t:f:s:e:c:d:', ["input", "url", "number", "max", "tag", "filter", "start", "end", "contain", "delete"])
    except getopt.GetoptError, err:
        print str(err)
        sys.exit(2)


    for o, a in opts:
        if o in ('-i', '--input'):
            source = a
        if o in ('-u', '--url'):
            source = a
        if o in ('-n', '--number'):
            keyword_min_number = int(a)
        if o in ('-m', '--max'):
            keyword_max_number = int(a)
        if o in ('-t', '--tag'):
            custom_html_tag = a
        if o in ('-f', '--filter'):
            custom_filter = a
        if o in ('-s', '--start'):
            start = int(a)
        if o in ('-e', '--end'):
            end = int(a)
        if o in ('-c', '--contain'):
            custom_contain = a
        if o in ('-d', '--delete'):
            delete_from_char = a

    if source == "":
        print "you must input the input file or dir"
        return

    convert(source)

if __name__ == '__main__':
    main(sys.argv)
    
