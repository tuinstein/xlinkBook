#!/usr/bin/env python

from extensions.bas_extension import BaseExtension
from config import Config
from utils import Utils
from record import Record
from knowledgegraph import KnowledgeGraph
import os

class Exclusive(BaseExtension):

    def __init__(self):
        BaseExtension.__init__(self)
        self.utils = Utils()
        self.kg = KnowledgeGraph()

    def excute(self, form_dict):
        rID = form_dict['rID'].strip()
        title = form_dict['rTitle'].replace('%20', ' ').strip()
        #fileName = form_dict['fileName']
        url = form_dict['url'].strip()
        fileName = form_dict['originFileName']
        print fileName
        if rID.startswith('loop-h'):
            historyPath = os.getcwd() + '/extensions/history/data/' + fileName[fileName.rfind('/') + 1 :] + '-history' 
            print historyPath
            r = self.utils.getRecord(title, path=historyPath, matchType=2, use_cache=False, accurate=False)
        else:
            r = self.utils.getRecord(rID, path=fileName)

        if r != None and r.get_id().strip() != '':

            if rID.startswith('loop-h'):
                title = title.replace('%20', ' ')
                desc = r.get_describe() + ' ' + self.kg.getCrossref(title, ' '.join(Config.exclusive_crossref_path))
                record = Record('custom-exclusive-' + rID + ' | '+ title + ' | ' + url + ' | ' + desc)
                localUrl = self.utils.output2Disk([record], 'exclusive', 'exclusive')

            else:
                db = fileName[fileName.find('db/') + 3 : fileName.rfind('/')] + '/'
                key = fileName[fileName.rfind('/') + 1 :]
                print db + ' ' + key
                #return 'http://' + Config.ip_adress + '/?db=' + db + '&key=' + key + '&filter=' + title.replace('...', '') + '&column=1'
                localUrl = 'http://' + Config.ip_adress + '/?db=' + db + '&key=' + key + '&filter=' + rID + '&column=1&enginType='  + Config.recommend_engin_type

            localUrl = localUrl + '&crossrefQuery=""'
            return self.getUrl(r.get_url(), localUrl)
        else:
            title = title.replace('%20', ' ')
            desc = 'engintype:' + title + ' '
            desc += 'localdb:' + title + ' '
            desc += self.kg.getCrossref(title, ' '.join(Config.exclusive_crossref_path))
            record = Record('custom-exclusive-' + rID + ' | '+ title + ' | ' + url + ' | ' + desc)
            localUrl = self.utils.output2Disk([record], 'exclusive', 'exclusive')
            localUrl = localUrl + '&crossrefQuery=""'
            return self.getUrl(url, localUrl)

        #if fileName.find("/custom") != -1:
        #    fileName = form_dict['originFileName']
        #if form_dict.has_key('fileName') and form_dict['fileName'] != '':
        #    fileName = form_dict['fileName']

    def getUrl(self, url, localUrl):
        for k, v in Config.exclusive_default_tab.items():
            if url.find(k) != -1:
                localUrl += '&extension=' + v
                break
        return localUrl  

    def check(self, form_dict):
	    column = str(form_dict['column']).strip()
        #print 'exclusive check column ' + column
	    return True
