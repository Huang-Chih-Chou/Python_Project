# -*- coding: UTF-8 -*- 
'''
Created on 2016-10-10
@author :   dillon
'''
import httplib
conn = httplib.HTTPSConnection("www.python.org")
conn.request("GET", "/")
r1 = conn.getresponse()
print r1.status, r1.reason
data1 = r1.read()
print data1