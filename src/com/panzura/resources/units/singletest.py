import unittest
import logging
from resources.pages.login import LoginPage
from resources.pages.page import Page
import inspect
from boto.dynamodb.condition import NULL

logging.basicConfig()
log = logging.getLogger()
log.setLevel('DEBUG')


class singletest(unittest.TestCase):
    apikey = None
    
    @classmethod
    def setUpClass(cls):
        lp = LoginPage()
        (statusCode, singletest.apikey) = lp.login()
#        self.assertEqual(200, statusCode, 'Failed to get apikey, stop the entire test suite.')
    
    def getCurrentFunctionName(self):
        return inspect.stack()[1][3]
    
    def logInfo(self, msg=None):
        detaledMsg = "%s.%s invoked >> %s" % (self.__class__.__name__, self.getCurrentFunctionName(), msg)
        log.info(detaledMsg)
    
    def log(self, msg=None):
        log.info(msg)
        
    def assertTrue(self, expr, msg=None):
        """ if expr is true will pass, otherwise will fail test case and print msg"""
        unittest.TestCase.assertTrue(self, expr, msg=msg)
        
    def assertFalse(self, expr, msg=None):
        """ if expr is false will pass, otherwise will fail test case and print msg"""
        unittest.TestCase.assertFalse(self, expr, msg=msg)
    
    def assertEqual(self, first, second, msg=None):
        """ if first equals second will pass, otherwise will fail test case and print msg"""
        unittest.TestCase.assertEqual(self, first, second, msg=msg)
        
    def assertIn(self, member, container, msg=None):
        """ if member is contained by container will pass, otherwise will fail test case and print msg"""
        unittest.TestCase.assertIn(self, member, container, msg=msg)
    
        