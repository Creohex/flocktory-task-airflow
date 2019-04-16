import importlib
import common
from log_analyzer import analyze_hourly, analyze_indicents
import os, psycopg2, unittest, time
from datetime import datetime
from dateutil import parser


class TestHelpers(unittest.TestCase):
    def test_datetime_hour_truncated(self):
        self.assertEqual(
            common.datetime_hour_truncated(
                parser.parse('2019-12-25 02:30:45')),
            parser.parse('2019-12-25 02:00:00'))

    def test_is_datetime_hour_truncated(self):
        self.assertFalse(common.is_datetime_hour_truncated(
            parser.parse('2019-12-25 02:30:45')))
        self.assertTrue(common.is_datetime_hour_truncated(
            parser.parse('2019-12-25 00:00:00')))
    
    def test_get_env_vars(self):
        # expect not having all required variables
        with self.assertRaises(Exception) as context:
            common.get_env_vars()
            self.assertTrue('missing required variables' in str(context.exception))
        
        # manually add required variables
        for _ in ['PGHOST', 'PGUSER', 'PGPORT', 'PGPASSWORD', 'PGDATABASE', 'E']:
            os.environ[_] = 'qwerty'

        # expect function to succeed
        common.get_env_vars()


class TestDb(unittest.TestCase):
    def test_get_connection(self):
        print(common.get_env_vars())
        common.get_connection()

    def test_query_db(self):
        self.assertEqual((True, [(1,)]), common.query_db("select 1"))

class TestLogAnalyzer(unittest.TestCase):
    def test_analyze_hourly(self):
        pass
    
    def test_analyze_incidents(self):
        pass


if __name__ == '__main__':
    unittest.main()
