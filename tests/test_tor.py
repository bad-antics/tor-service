import unittest,sys,os
sys.path.insert(0,os.path.join(os.path.dirname(__file__),"..","src"))
from tor_service.core import TorChecker,HiddenService

class TestChecker(unittest.TestCase):
    def test_init(self):
        c=TorChecker()
        self.assertIsNotNone(c)

class TestHidden(unittest.TestCase):
    def test_torrc(self):
        hs=HiddenService()
        cfg=hs.generate_torrc("/tmp/hs")
        self.assertIn("HiddenServiceDir",cfg)

if __name__=="__main__": unittest.main()
