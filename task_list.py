from PyQt5.QtCore import QEvent
from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QStyle
from PyQt5.QtWidgets import QStyleOptionViewItem
from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5.QtWidgets import QTableView, QWidget, QPushButton
from PyQt5.QtWidgets import QVBoxLayout, QFormLayout, QHBoxLayout

from model import Task, TaskModel


class Delegate(QStyledItemDelegate):
    def __init__(self, view):
        super().__init__()
        self.select_row = None
        self.view = view

    # def paint(self, painter, option, index):
    #     """ paint(self, QPainter, QStyleOptionViewItem, QModelIndex) """
    #     is_over = option.state & QStyle.State_MouseOver
    #     a = QStyleOptionViewItem()
    #     if is_over and self.select_row != index.row():
    #         self.select_index = index.row()
    #         print(self.select_index)
    #         self.view.select(index.row())
    #
    #     super().paint(painter, option, index)

class TaskTableWidget(QTableView):
    def __init__(self):
        super().__init__()
        self.setColumnWidth(0, 40)
        self.horizontalHeader().setStretchLastSection(True)

        # headers
        self.horizontalHeader().hide()
        self.verticalHeader().hide()

        # select current row
        self.setFocusPolicy(Qt.NoFocus)
        self.setMouseTracking(True)
        self.current_row = 0
        # self.viewport()
        # self.cellEntered.connect(self.cell_hover)
        self._row_unselect_brush = QBrush(QColor('white'))
        self._row_select_brush = QBrush(QColor(255, 235, 160))
        # self.delegate = Delegate(self)
        # self.setItemDelegate(self.delegate)
        self.sel_row = None
        # self.setStyleSheet("""
        # QTableView::indicator:hover {
        #     background: #FFEBA0;
        # }
        # """)

    def mouseMoveEvent(self, event):
        #     QMouseEvent
        index = self.indexAt(event.pos())
        if index.isValid() and self.sel_row != index.row():
            self.sel_row = index.row()
            # self.model().select(self.sel_row)

    # def select(self, row):
    #     self.model().select(row)

    def cell_hover(self, row, column):
        if self.current_row != row:
            old = self.current_row
            self.item(row, 0).setBackground(self._row_select_brush)
            self.item(row, 1).setBackground(self._row_select_brush)
            self.item(old, 0).setBackground(self._row_unselect_brush)
            self.item(old, 1).setBackground(self._row_unselect_brush)
            self.current_row = row

    def setTasks(self, tasks):
        self.setModel(TaskModel(tasks))


class TaskList(QWidget):
    open = pyqtSignal(Task)

    def __init__(self):
        super().__init__()
        self.table = TaskTableWidget()
        self.init_ui()

    def create_task_table(self, rows):
        tasks = []
        for row in range(rows):
            tasks.append(Task('Text%d' % row, False))

        self.table.setTasks(tasks)

        # self.table.itemClicked.connect(self.handle_item_clicked)
        return self.table

    def handle_item_clicked(self, item):
        if item.checkState() == Qt.Checked:
            print('"%s" Checked' % item.text())
        else:
            self.open.emit(item.task)

    def create_main_form(self):
        fm = QFormLayout()
        fm.addRow(self.create_task_table(5))

        return fm

    def create_control_buttons(self):
        control_lt = QHBoxLayout()

        btn_save = QPushButton('Добавить задачу')
        control_lt.addWidget(btn_save, 0, Qt.AlignCenter)

        btn_cancel = QPushButton('с датой')
        control_lt.addWidget(btn_cancel, 0, Qt.AlignCenter)

        return control_lt

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addLayout(self.create_main_form())
        layout.addStretch()
        layout.addLayout(self.create_control_buttons())
        self.setLayout(layout)
