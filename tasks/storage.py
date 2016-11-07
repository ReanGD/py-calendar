from PyQt5.QtCore import QDate, QTime, QDateTime


class Task(object):
    def __init__(self, desc, datetime, completed):
        super().__init__()
        self.desc = desc
        self.datetime = datetime
        self.completed = completed


class TaskStorage(object):
    def __init__(self):
        self.data = []

    def load(self):
        data = []
        for row in range(10):
            date = QDate().currentDate().addDays(row)
            h = row
            m = 0
            time = QTime(h, m)
            datetime = QDateTime(date, time)
            data.append(Task('Text%d' % row, datetime, False))

        return data