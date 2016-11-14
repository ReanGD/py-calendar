from os import path
from datetime import datetime
from unittest import TestCase
from dateutil.tz import tzlocal

from ical.database import Database
from ical.exception import ICalException


class TestDatabase(TestCase):
    @staticmethod
    def db_path(calendar_name):
        root_path = path.dirname(path.dirname(path.realpath(__file__)))
        return path.join(root_path, 'test_data', calendar_name + '.ics')

    @staticmethod
    def read_db(calendar_name):
        cal = Database(TestDatabase.db_path(calendar_name))
        cal.load()
        return cal.enumerate(datetime(2017, 1, 1))

    def test_failed_path(self):
        cal = Database('error.ics')
        with self.assertRaises(ICalException):
            cal.load()

    def test_failed_file(self):
        cal = Database(TestDatabase.db_path('error'))
        with self.assertRaises(ICalException):
            cal.load()

    def test_todo(self):
        for it in TestDatabase.read_db('todo'):
            if it.summary == 'only summary':
                self.assertIsNone(it.dtstart)
                self.assertIsNone(it.status)
                self.assertIsNone(it.completed_at)
                self.assertFalse(it.is_completed)
            elif it.summary == 'with dtstart':
                self.assertEqual(datetime(2016, 1, 1, hour=1, tzinfo=tzlocal()), it.dtstart)
                self.assertIsNone(it.status)
                self.assertIsNone(it.completed_at)
                self.assertFalse(it.is_completed)
            elif it.summary == 'in process':
                self.assertIsNone(it.dtstart)
                self.assertEqual('IN-PROCESS', it.status)
                self.assertIsNone(it.completed_at)
                self.assertFalse(it.is_completed)
            elif it.summary == 'completed':
                self.assertIsNone(it.dtstart)
                self.assertEqual('COMPLETED', it.status)
                self.assertEqual(datetime(2016, 1, 1, tzinfo=tzlocal()), it.completed_at)
                self.assertTrue(it.is_completed)
            elif it.summary == 'cancelled':
                self.assertIsNone(it.dtstart)
                self.assertEqual('CANCELLED', it.status)
                self.assertIsNone(it.completed_at)
                self.assertTrue(it.is_completed)
            else:
                self.fail('unknown item')
