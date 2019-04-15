from common import *
from log_analyzer import analyze_hourly, analyze_indicents
import os, psycopg2, unittest


# TODO: ...
# common:
class TestCommonMethods(unittest.TestCase):
    def test_datetime_hour_truncated(self):
        self.assertTrue(True)
        pass

    def test_is_datetime_hour_truncated(self):
        self.assertTrue(False)
        pass


# TODO: ...
# log_analyzer:
class TestCommonMethods(unittest.TestCase):
    def test_analyze_hourly(self):
        pass
    
    def test_analyze_incidents(self):
        pass


if __name__ == '__main__':
    unittest.main()
