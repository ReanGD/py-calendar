from datetime import datetime
from unittest import TestCase

from os import path

from ical.database import Database
from ical.exception import ICalException


class TestDatabase(TestCase):
    def db_path(self, calendar_name):
        root_path = path.dirname(path.dirname(path.realpath(__file__)))
        return path.join(root_path, 'test_data', calendar_name + '.ics')

    def read_db(self, calendar_name):
        cal = Database(self.db_path(calendar_name))
        cal.load()
        return cal.enumerate(datetime(2017, 1, 1))

    def test_failed_path(self):
        with self.assertRaises(ICalException):
            Database('error.ics')

    def test_failed_file(self):
        cal = Database(self.db_path('error'))
        with self.assertRaises(ICalException):
            cal.load()

    def test_todo(self):
        for it in self.read_db('todo'):
            if it.summary == 'only summary':
                self.assertIsNone(it.dtstart)
                self.assertIsNone(it.status)
            elif it.summary == 'with dtstart':
                self.assertEqual(datetime(2016, 1, 1, hour=1), it.dtstart)
                self.assertIsNone(it.status)
            elif it.summary == 'in process':
                self.assertIsNone(it.dtstart)
                self.assertEqual('IN-PROCESS', it.status)
            else:
                self.fail('unknown item')
