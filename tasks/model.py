from PyQt5.QtCore import QAbstractTableModel, QVariant, Qt
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QColor

from tasks.storage import TaskStorage


class TaskModel(QAbstractTableModel):
    col_completed = 0
    col_desc = 1
    col_date = 2

    def __init__(self):
        super().__init__()
        storage = TaskStorage()
        self.tasks = storage.load()
        self._selected_row = None
        self._brush_row = QBrush(QColor('white'))
        self._brush_row_selected = QBrush(QColor(255, 235, 160))

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.tasks)

    def columnCount(self, parent=None, *args, **kwargs):
        return 3

    def data(self, index, role=None):
        skip_role = [Qt.DecorationRole, Qt.FontRole,
                     Qt.TextAlignmentRole, Qt.BackgroundRole,
                     Qt.ForegroundRole]
        if not index.isValid() or role in skip_role:
            return QVariant()

        # if role == Qt.BackgroundRole:
            # print(self._selected_row, ':', index.row())
            # if self._selected_row == index.row():
            #     return self._brush_row_selected
            # else:
            #     return self._brush_row
        # else:
        #     print(self._selected_row, ':', index.row(), '!')

        task = self.tasks[index.row()]
        col = index.column()

        if role == Qt.CheckStateRole:
            if col == TaskModel.col_completed:
                return Qt.Checked if task.completed else Qt.Unchecked
        elif role == Qt.DisplayRole:
            if col == TaskModel.col_desc:
                return task.desc
        elif role == Qt.EditRole:
            if col == TaskModel.col_desc:
                return task.desc
            elif col == TaskModel.col_date:
                return task.datetime.date()

        else:
            return QVariant()

    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid():
            return False

        col = index.column()
        if role == Qt.CheckStateRole:
            if col == TaskModel.col_completed:
                self.tasks[index.row()].completed = (value == Qt.Checked)
                return True

        if role == Qt.EditRole:
            if col == TaskModel.col_desc:
                self.tasks[index.row()].desc = value
                return True
            elif col == TaskModel.col_date:
                self.tasks[index.row()].datetime.setDate(value)
                return True

        return False

    def removeRow(self, row, parent=None, *args, **kwargs):
        if row >= 0 and row < self.rowCount():
            del self.tasks[row]
            return True

        return False

    # def select(self, row):
    #     self._selected_row = row
    #     self.dataChanged.emit(self.createIndex(row, 0),
    #                           self.createIndex(row, 1),
    #                           [Qt.BackgroundRole])

    def flags(self, index):
        if index.isValid():
            if index.column() == TaskModel.col_completed:
                return Qt.ItemIsUserCheckable | Qt.ItemIsEnabled
            elif index.column() == TaskModel.col_desc:
                return Qt.ItemIsEnabled

        return super().flags(index)
