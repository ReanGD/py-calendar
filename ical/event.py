import icalendar
import dateutil.rrule as rrule
from datetime import date, datetime, time

from dateutil.tz import tzlocal

from ical.exception import ICalException


_localtimezone = tzlocal()


def _normalize_date(val) -> datetime:
    if val is None:
        return None
    elif isinstance(val, date) and not isinstance(val, datetime):
        return datetime(val.year, val.month, val.day, tzinfo=_localtimezone)
    elif isinstance(val, time):
        raise ICalException('data field exist only time without date')

    if not val.tzinfo:
        val = val.replace(tzinfo=_localtimezone)

    return val


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

    def enumerate(self, before: datetime):
        dtstart = _normalize_date(self.root.decoded('DTSTART', None))
        before = _normalize_date(before)

        if len(self.children) == 0:
            if dtstart is None or dtstart < before:
                return [Event(self, self.root)]
            else:
                return []

        events = []
        for dt in self.rrule.between(dtstart, before):
            if dt in self.children:
                events.append(Event(self, self.children[dt]))
            else:
                events.append(Event(self, self.root, dt))

        return events


class Event(object):
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
    def dtstart(self) -> datetime:
        """This property specifies when the calendar component begins."""
        if self._dtstart is not None:
            return self._dtstart
        else:
            return _normalize_date(self.data.decoded('DTSTART', None))

    @property
    def status(self) -> icalendar.prop.vText:
        """This property defines the overall status or confirmation for the calendar component."""
        return self.data.get('STATUS')

    @property
    def completed_at(self) -> datetime:
        """This property defines the date and time that a to-do was actually completed."""
        return _normalize_date(self.data.decoded('COMPLETED', None))

    @property
    def is_completed(self) -> bool:
        return self.status in ('CANCELLED', 'COMPLETED') or bool(self.completed_at)

