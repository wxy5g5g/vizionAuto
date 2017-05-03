import logging
import inspect
import exceptions
import sys
import unittest


log = logging.getLogger()
log.setLevel('DEBUG')

class Page(object):
    
    def getCurrentFunctionName(self):
        return inspect.stack()[1][3]
    
    def logInfo(self, msg=None):
        detaledMsg = "%s.%s invoked >> %s" % (self.__class__.__name__, self.getCurrentFunctionName(), msg)
        log.info(detaledMsg)
