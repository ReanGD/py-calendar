import icalendar
from typing import List
from dateutil.tz import tzlocal
import dateutil.rrule as rrule
from datetime import date, datetime, time


class Entity(object):
    def __init__(self, obj):
        super().__init__()
        self.root = None
        self.rrule = None
        self.children = dict()
        self.add(obj)

    def add(self, obj: icalendar.cal.Component):
        uid = obj['UID']
        if 'RECURRENCE-ID' not in obj:
            if self.root is not None:
                raise Exception('double root initialization for uid="%s"' % uid)
            self.root = obj
            if 'RRULE' in obj:
                rrulestr = obj['RRULE'].to_ical().decode('utf-8')
                self.rrule = rrule.rrulestr(rrulestr, dtstart=obj.decoded('DTSTART'))
                if not {'UNTIL', 'COUNT'}.intersection(obj['RRULE'].keys()):
                    # pytz.timezones don't know any transition dates after 2038 either
                    self.rrule._until = datetime(2038, 12, 31)
                elif self.rrule._until.tzinfo:
                    self.rrule._until = self.rrule._until.replace(tzinfo=None)
        else:
            self.children[obj.decoded('RECURRENCE-ID')] = obj

    def enumerate(self, until: datetime):
        #  -> List[Event]
        if len(self.children) == 0:
            return [Event(self, self.root)]

        events = []
        for dt in self.rrule.between(self.root.decoded('DTSTART'), until):
            if dt in self.children:
                events.append(Event(self, self.children[dt]))
            else:
                events.append(Event(self, self.root, dt))

        return events


# состояние
# повтор

class Event(object):
    _localtimezone = tzlocal()

    def __init__(self, root, event: icalendar.Event, dtstart=None):
        super().__init__()
        self.root = root
        self.data = event
        self._dtstart = dtstart

    @property
    def summary(self) -> icalendar.prop.vText:
        """This property defines a short summary or subject for the calendar component."""
        return self.data.get('SUMMARY', icalendar.prop.vText(''))

    @property
    def description(self) -> icalendar.prop.vText:
        """This property provides a more complete description of the calendar component,
        than that provided by the "SUMMARY" property."""
        return self.data.get('DESCRIPTION', icalendar.prop.vText(''))

    @property
    def dtstart(self):
        """This property specifies when the calendar component begins."""
        if self._dtstart is not None:
            return self._dtstart
        else:
            # normalize_datetime
            return self.data.decoded('dtstart')

    def _set_field(self, name, value):
        if name in self.data:
            del (self.data[name])
        if value is not None and value is not '':
            self.data.add(name, value)

    @summary.setter
    def summary(self, value):
        self._set_field('summary', value)

    @property
    def status(self):
        return self.data.get('status', 'NEEDS-ACTION')

    @property
    def is_completed(self):
        return bool(self.completed_at) or \
               self.status in ('CANCELLED', 'COMPLETED')

    @property
    def completed_at(self):
        if self.data.get('completed', None) is None:
            return None
        else:
            return self.data.decoded('completed')

    def __repr__(self):
        return 'summary: "{}", description: "{}"'.format(self.summary, self.description)
