from dateutil.tz import tzlocal
from datetime import date, datetime, time
import icalendar


_localtimezone = tzlocal()


def check_fields(obj: icalendar.cal.Component):
    uid = obj['UID']
    if uid is None or uid == '':
        raise Exception('not found field "UID"')

    if 'DTSTART' not in obj:
        raise Exception('not found field "DTSTART" for uid="%s"' % uid)



def normalize_datetime(val):
    if isinstance(val, date) and not isinstance(val, datetime):
        val = datetime(val.year, val.month, val.day)
    elif isinstance(val, time):
        val = datetime.combine(date.today(), val)

    if not val.tzinfo:
        val = val.replace(tzinfo=_localtimezone)

    return val