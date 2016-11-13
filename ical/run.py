from os import path
from datetime import datetime
from ical.database import Database

root_path = path.dirname(path.dirname(path.realpath(__file__)))
cal = Database(path.join(root_path, 'calendars', 'default.ics'))
cal.load()
for item in cal.enumerate(datetime(2016, 11, 20)):
    print(item)
