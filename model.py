from PyQt5.QtCore import QAbstractTableModel, QVariant, Qt
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QColor


class Task(object):
    def __init__(self, desk, completed):
        super().__init__()
        self.desk = desk
        self.completed = completed


class TaskModel(QAbstractTableModel):
    def __init__(self, tasks):
        super().__init__()
        self.tasks = tasks
        self._selected_row = None
        self._brush_row = QBrush(QColor('white'))
        self._brush_row_selected = QBrush(QColor(255, 235, 160))

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.tasks)

    def columnCount(self, parent=None, *args, **kwargs):
        return 2

    def data(self, index, role=None):
        if not index.isValid():
            return QVariant()

        if role == Qt.BackgroundRole:
            # print(self._selected_row, ':', index.row())
            if self._selected_row == index.row():
                return self._brush_row_selected
            else:
                return self._brush_row
        # else:
        #     print(self._selected_row, ':', index.row(), '!')

        task = self.tasks[index.row()]
        col = index.column()

        if role == Qt.CheckStateRole:
            if col == 0:
                return Qt.Checked if task.completed else Qt.Unchecked
        elif role == Qt.DisplayRole:
            if col == 1:
                return task.desk
        else:
            return QVariant()

    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid():
            return False

        if role == Qt.CheckStateRole and index.column() == 0:
            self.tasks[index.row()].completed = (value == Qt.Checked)
            return True

        return False

    def select(self, row):
        self._selected_row = row
        self.dataChanged.emit(self.createIndex(row, 0),
                              self.createIndex(row, 1),
                              [Qt.BackgroundRole])

    def flags(self, index):
        if index.isValid():
            if index.column() == 0:
                return Qt.ItemIsUserCheckable | Qt.ItemIsEnabled
            elif index.column() == 1:
                return Qt.ItemIsEnabled

        return super().flags(index)
