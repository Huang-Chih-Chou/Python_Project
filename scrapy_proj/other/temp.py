#!/usr/bin/python
#coding:utf-8
import urllib2

request = urllib2.Request("https://tw.yahoo.com/")
response = urllib2.urlopen(request)
html = response.read()
print html