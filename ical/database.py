import datetime
import os
import icalendar
from typing import List, Dict

from atomicwrites import AtomicWriter

from ical.event import Entity, Event
from ical.exception import ICalException


class Database(object):
    def __init__(self, path: str):
        super().__init__()
        self.path = path
        self._data = {}

    @staticmethod
    def _load(path: str):
        if not os.path.isfile(path):
            raise ICalException('Calendar file "{}" is not exists'.format(path))

        cal = icalendar.Calendar.from_ical(open(path, 'rb').read())
        data = {}
        for item in cal.walk():
            if item.name == 'VTODO':
                uid = item.get('UID')
                if uid is None or uid == '':
                    raise Exception('not found field "UID"')

                if uid in data:
                    data[uid].add(item)
                    raise Exception('Not supported recurring events')
                else:
                    data[uid] = Entity(item)

        return data

    def load(self):
        try:
            self._data = Database._load(self.path)
        except Exception as e:
            raise ICalException('Failed to load calendar "{}": {}'.format(self.path, e))

    @staticmethod
    def _save(path: str, data: Dict[str, Entity]):
        if os.path.isfile(path):
            cal = icalendar.Calendar.from_ical(open(path, 'rb').read())
            exists = set()
            for index, component in enumerate(cal.subcomponents):
                uid = component.get('UID')
                if uid in data and data[uid].pre_save():
                    exists.add(uid)
                    cal.subcomponents[index] = data[uid].root

            for uid, it in data:
                if uid not in exists:
                    cal.add_component(it.root)

            with AtomicWriter(path, overwrite=True).open() as f:
                f.write(cal.to_ical().decode("UTF-8"))
        else:
            cal = icalendar.Calendar()
            cal.add('prodid', 'py-calendar')
            cal.add('version', '2.0')
            for it in data.values():
                it.pre_save()
                cal.add_component(it.root)

            with AtomicWriter(path).open() as f:
                f.write(cal.to_ical().decode("UTF-8"))

    def save(self):
        try:
            Database._save(self.path, self._data)
        except Exception as e:
            raise ICalException('Failed to save calendar "{}": {}'.format(self.path, e))

    def enumerate(self, before: datetime) -> List[Event]:
        events = []
        for it in self._data.values():
            events.extend(it.enumerate(before))
        return events
