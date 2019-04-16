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

        # expect to get all required environment variables
        self.assertTrue(
            all(key in ("PGHOST", "PGUSER", "PGPORT", "PGPASSWORD", "PGDATABASE", "E") 
                for key in common.get_env_vars()))

class TestDb(unittest.TestCase):
    @staticmethod
    def prepare_logs():
        common.query_db("INSERT INTO logs (timestamp, level, message) VALUES "
            "('1970-01-1 01:15:00', 'INFO', 'text1'), "
            "('1970-01-1 01:30:45', 'DEBUG', 'text2'), "
            "('1970-01-1 02:15:09', 'ERROR', 'text3')")
    
    @staticmethod
    def cleanup_logs():
        common.query_db("DELETE FROM logs "
            "WHERE timestamp='1970-01-1 01:15:00' "
                "OR timestamp='1970-01-1 01:30:45' "
                "OR timestamp='1970-01-1 02:15:09'")
    
    @staticmethod
    def prepare_hourly():
        pass
    
    @staticmethod
    def cleanup_hourly():
        pass
    
    @staticmethod
    def prepare_incidents():
        pass
    
    @staticmethod
    def cleanup_incidents():
        pass

    def test_get_connection(self):
        print(common.get_env_vars())
        common.get_connection()

    def test_query_db(self):
        self.assertEqual([(1,)], common.query_db("select 1"))
    
    def test_levels_operations(self):
        self.assertTrue(len(common.select_log_levels()) == 5)

    def test_log_operations(self):
        try:
            TestDb.prepare_logs()
            logs1 = common.select_logs(common.datetime_hour_truncated(parser.parse('1970-01-1 01:15:00')))
            self.assertTrue(len(logs1) == 2)
            logs2 = common.select_logs(common.datetime_hour_truncated(parser.parse('1970-01-1 02:15:09')))
            self.assertTrue(len(logs2) == 1)
        except Exception as e:
            raise
        finally:
            TestDb.cleanup_logs()
        
    def test_hourly_operations(self):
        pass
    
    def test_incidents_operations(self):
        pass


class TestLogAnalyzer(unittest.TestCase):
    def test_analyze_hourly(self):
        pass
    
    def test_analyze_incidents(self):
        pass


if __name__ == '__main__':
    unittest.main()
