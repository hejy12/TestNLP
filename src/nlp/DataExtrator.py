# -*- coding: utf-8 -*-
'''
Created on 2015年11月23日

@author: Hk
'''
from xml.dom import minidom

class DataExtrator(object):

    @staticmethod
    def getAttrValue(node, attrname):
        return node.getAttribute(attrname) if node else ''
    
    @staticmethod
    def getNodeValue(node, index=0):
        return node.childNodes[index].nodeValue if node else ''
    
    @staticmethod
    def getXMLNode(node, name):
        return node.getElementsByTagName(name) if node else []
    
    @staticmethod
    def xml2String(filename='user.xml'):
        doc = minidom.parse(filename)
        return doc.toxml('UTF-8')

