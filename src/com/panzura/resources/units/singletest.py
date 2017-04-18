import unittest
import logging


logging.basicConfig()
log = logging.getLogger()
log.setLevel('INFO')


class singletest(unittest.TestCase):
    apikey = None
    
    
    def assertTrue(self, expr, msg=None):
        unittest.TestCase.assertTrue(self, expr, msg=msg)
        
    def assertFalse(self, expr, msg=None):
        unittest.TestCase.assertFalse(self, expr, msg=msg)
        
    def logInfo(self,msg=None):
        log.info(msg)