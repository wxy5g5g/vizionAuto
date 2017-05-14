from xml.dom import minidom
import logging
import os

log = logging.getLogger()
log.setLevel('INFO')


class Property():

    @staticmethod
    def getProperties(fieldName):     
        cccXmlPath = "/opt/workspace/CCC_api_test_demo/src/com/panzura/resources/properties/ccc.xml"
#        cccXmlPath = "../resources/properties/ccc.xml"
     
        dom = minidom.parse(cccXmlPath)
        root = dom.documentElement
        try:
            ccc = dom.getElementsByTagName(fieldName)
        except Exception,e:
            log.info("Get property failed since" + e)   
        value = ccc[0].firstChild.data
        return value