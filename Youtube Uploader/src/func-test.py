# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 09:41:17 2012

@author: wkentler
"""

def funcA(text):
    print 'funcA: %s' % text
    
    
    def funcB(text):
        print 'funcB: %s' % text
        
    def funcC(text):
        print 'funcC: %s' % text
        
    funcB(text)    
        
        
funcA('OOOOhhhh')
