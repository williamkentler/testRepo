# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 09:13:08 2012

@author: wkentler
"""

import urllib, threading


class FileGetter(threading.Thread):
    def __init__(self, url):
        self.url = url
        self.result = None
        threading.Thread.__init__(self)
        
        
     def get_result(self):
         return self.result
         
    def run(self)
        try:
            f = urllib.urlopen(url)
            contents = f.read()
            f.close
            self.result = contents
        except IOError:
            print 'could not get the file %s' % url
        
        

from Queue import Queue

def get_files(files):
    def producer
