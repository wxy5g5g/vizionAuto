import unittest
import logging
from resources.pages.login import LoginPage
from resources.pages.page import Page
import inspect

logging.basicConfig()
log = logging.getLogger()
log.setLevel('INFO')


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
    
    def assertTrue(self, expr, msg=None):
        unittest.TestCase.assertTrue(self, expr, msg=msg)
        
    def assertFalse(self, expr, msg=None):
        unittest.TestCase.assertFalse(self, expr, msg=msg)
    
    def assertEqual(self, first, second, msg=None):
        unittest.TestCase.assertEqual(self, first, second, msg=msg)
        
    def assertIn(self, member, container, msg=None):
        unittest.TestCase.assertIn(self, member, container, msg=msg)
        