from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5.QtWidgets import QTableView, QWidget, QPushButton
from PyQt5.QtWidgets import QVBoxLayout, QFormLayout, QHBoxLayout


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
    def __init__(self, model):
        super().__init__()
        self.setModel(model)
        self.setColumnWidth(0, 40)
        self.horizontalHeader().setStretchLastSection(True)

        # Columns
        self.setColumnHidden(2, True)

        # headers
        self.horizontalHeader().hide()
        self.verticalHeader().hide()

        # select current row
        self.setFocusPolicy(Qt.NoFocus)
        self.setMouseTracking(True)
        self.current_row = 0
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
        index = self.indexAt(event.pos())
        if index.isValid() and self.sel_row != index.row():
            self.sel_row = index.row()

    def mouseReleaseEvent(self, event):
        index = self.indexAt(event.pos())
        self.parentWidget().open.emit(index.row())


class TaskList(QWidget):
    open = pyqtSignal(int)

    def __init__(self, model):
        super().__init__()
        self.table = TaskTableWidget(model)
        self.init_ui()

    def create_main_form(self):
        fm = QFormLayout()
        fm.addRow(self.table)

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
