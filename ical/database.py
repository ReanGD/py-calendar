import datetime
import os
import icalendar
from typing import List

from ical.event import Entity, Event


class Database(object):
    def __init__(self, path: str):
        super().__init__()
        if not os.path.isfile(path):
            raise Exception('Calendar file "{}" is not exists'.format(path))

        self._calendar_path = path
        self._data = dict()

    @staticmethod
    def _load(path):
        cal = icalendar.Calendar.from_ical(open(path, 'rb').read())
        data = dict()
        for item in cal.walk():
            if item.name == 'VTODO':
                uid = item.get('UID')
                if uid is None or uid == '':
                    raise Exception('not found field "UID"')

                if uid in data:
                    data[uid].add(item)
                else:
                    data[uid] = Entity(item)

        return data

    def load(self):
        try:
            self._data = Database._load(self._calendar_path)
        except Exception as e:
            raise Exception('Failed to load calendar "{}": {}'.format(self._calendar_path, e))

    def enumerate(self, until: datetime) -> List[Event]:
        events = []
        for it in self._data.values():
            events.extend(it.enumerate(until))
        return events
