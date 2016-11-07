class Task(object):
    def __init__(self, desk, completed):
        super().__init__()
        self.desk = desk
        self.completed = completed


class TaskStorage(object):
    def __init__(self):
        self.data = []

    def load(self):
        data = []
        for row in range(10):
            data.append(Task('Text%d' % row, False))

        return data