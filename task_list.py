from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QTableView, QWidget, QPushButton
from PyQt5.QtWidgets import QVBoxLayout, QFormLayout, QHBoxLayout


class TaskTableWidget(QTableView):
    def __init__(self, model):
        super().__init__()
        # self.setStyleSheet("""
        # QTableView::item:selected {
        #     selection-background-color: yellow;
        #     selection-color: black;
        #     show-decoration-selected: 0;
        # }
        # """)
        self.setModel(model)
        self.setColumnWidth(0, 40)
        self.horizontalHeader().setStretchLastSection(True)

        # Columns
        self.setColumnHidden(2, True)

        # headers
        self.horizontalHeader().hide()
        self.verticalHeader().hide()

        # selected row
        self.setFocusPolicy(Qt.NoFocus)
        # self.setSelectionBehavior(QAbstractItemView.SelectRows)
        # self.setSelectionMode(QAbstractItemView.SingleSelection)
        # self.selectRow(1)
        self.setMouseTracking(True)
        self.sel_row = None

    def mouseMoveEvent(self, event):
        index = self.indexAt(event.pos())
        if index.isValid() and self.sel_row != index.row():
            row = index.row()
            self.model().selected_row = row

            if self.sel_row is not None:
                rect1 = self.visualRect(self.model().createIndex(self.sel_row, 0))
                rect2 = self.visualRect(self.model().createIndex(self.sel_row, 1))
                self.viewport().update(rect1 | rect2)

            rect1 = self.visualRect(self.model().createIndex(row, 0))
            rect2 = self.visualRect(self.model().createIndex(row, 1))
            self.viewport().update(rect1 | rect2)

            self.sel_row = row


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
