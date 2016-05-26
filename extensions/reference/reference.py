#!/usr/bin/env python

import sys, os
from extensions.bas_extension import BaseExtension
from utils import Utils
from update.all_subject import default_subject
from record import ReferenceRecord
from semanticscholar import Semanticscholar

class Reference(BaseExtension):

    record_reference = {}
    html = ''

    def __init__(self):
        BaseExtension.__init__(self)
        self.utils = Utils()
        self.semanticscholar = Semanticscholar()

    def loadReference(self, filename, rID):
        if len(self.record_reference) != 0 and self.record_reference.has_key(rID):
            return
        name = 'extensions/reference/data/' + filename + '-reference'
        if os.path.exists(name):
            f = open(name, 'rU')
            all_lines = f.readlines()
            for line in all_lines:
                if line.startswith('#'):
                    continue
                record = ReferenceRecord(line)
                key = record.get_id().strip()
                if key != rID:
                    continue

                if self.record_reference.has_key(key):
                    self.record_reference[key].append(record)
                else:
                    self.record_reference[key] = [record]

        #for (k, v) in self.record_reference.items():
        #    print k

    def excute(self, form_dict):
      
        fileName = form_dict['fileName'].encode('utf8')
        rID = form_dict['rID'].encode('utf8')
        self.loadReference(self.formatFileName(fileName), rID)
        #print self.record_reference
        
        result = self.genReferenceHtml(rID) 
        if result != '':
            return result
        else:
            return self.genReferenceHtml2(self.semanticscholar.getReferences(form_dict['rTitle']))


    def check(self, form_dict):
        fileName = form_dict['fileName'].encode('utf8')
        rID = form_dict['rID'].encode('utf8')
        self.loadReference(self.formatFileName(fileName), rID)
        if self.record_reference.has_key(rID) or rID.startswith('arxiv'):
            return True
        return False
                

    def genReferenceHtml2(self, alist):
        return self.genMetadataHtml2(alist)
    
    def genMetadataHtml2(self, alist):
            self.html = '<div class="ref"><ol>'
            count = 0
            for r in alist:
                count += 1
                self.html += '<li><span>' + str(count) + '.</span>'
                if r[1] != '':
                    self.html += '<p>' + '<a target="_blank" href="' + r[1] + '">' + r[0] + '</a>' + '</p>'
                else:
                    self.html += '<p>' + r[0] + '</p>'
                self.html += '</li>'
            return self.html + "</div>"


    def genReferenceHtml(self, rID):
        return self.genMetadataHtml(rID)

    def genMetadataHtml(self, key):
        if self.record_reference.has_key(key):
            self.html = '<div class="ref"><ol>'
            count = 0
            for r in self.record_reference[key]:
                count += 1
                self.html += '<li><span>' + str(count) + '.</span>'
                self.html += '<p>' + self.genMetadataLink(r.get_title().strip(), r.get_url().strip()) + '</p>'
                self.html += '</li>'
            return self.html + "</div>"
        else:
            return ''


    def genMetadataLink(self, title, url):
        if url.find('[') != -1:
            ft = url.replace('[', '').replace(']', '').strip()
            r = self.utils.getRecord(ft, '','', False, False)
            key = r.get_path()[r.get_path().find(default_subject) + len(default_subject) + 1 :]
            url = 'http://localhost:5000?db=' + default_subject + '/&key=' + key + '&filter=' + ft  + '&desc=true'

        return self.genMetadataLinkEx(title, url)


    def genMetadataLinkEx(self, title, url):
        if title.find('<a>') != -1:
            title = title.replace('<a>', '<a target="_blank" href="' + url + '">')
        else:
            title = '<a target="_blank" href="' + url + '">' + title + '</a>'
        return title
