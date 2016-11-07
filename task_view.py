from PyQt5.QtCore import QDate, Qt, pyqtSignal
from PyQt5.QtWidgets import QDataWidgetMapper
from PyQt5.QtWidgets import QFormLayout, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QWidget, QLineEdit, QDateEdit, QComboBox, QPushButton, QLabel


class TaskView(QWidget):
    close = pyqtSignal()

    def __init__(self, model):
        super().__init__()
        self.header = QLabel('')
        self.desk = QLineEdit()
        self.date = QDateEdit()
        self.time = QComboBox()
        self.init_ui()

        self.mapper = QDataWidgetMapper()
        self.mapper.setModel(model)
        self.mapper.addMapping(self.desk, 1)
        self.mapper.toFirst()

    def set_task(self, index):
        self.mapper.setCurrentIndex(index)
        self.header.setText('РЕДАКТИРОВАНИЕ ЗАДАЧИ')
        # text = 'НОВАЯ ЗАДАЧА'

    def create_date(self):
        self.date.setDate(QDate().currentDate())
        self.date.setDisplayFormat('dd.MM.yyyy')
        self.date.setCalendarPopup(True)
        self.date.setFixedWidth(120)

        return self.date

    def create_date_buttons(self):
        date_lt = QHBoxLayout()

        btn_now = QPushButton('сегодня')
        btn_now.clicked.connect(lambda: self.date.setDate(QDate().currentDate()))
        date_lt.addWidget(btn_now, 0, Qt.AlignCenter)

        btn_tomorrow = QPushButton('завтра')
        btn_tomorrow.clicked.connect(lambda: self.date.setDate(QDate().currentDate().addDays(1)))
        date_lt.addWidget(btn_tomorrow, 0, Qt.AlignCenter)

        btn_week_later = QPushButton('через неделю')
        btn_week_later.clicked.connect(lambda: self.date.setDate(QDate().currentDate().addDays(7)))
        date_lt.addWidget(btn_week_later, 0, Qt.AlignCenter)

        return date_lt

    def create_time_choice(self):
        self.time.setMaxVisibleItems(15)
        self.time.setStyleSheet('QComboBox { combobox-popup: 0; }')
        for it in range(24):
            self.time.insertItem(it * 2 + 0, '%.2d:00' % it)
            self.time.insertItem(it * 2 + 1, '%.2d:30' % it)

        return self.time

    def save(self):
        print('save', self.mapper.submit())
        self.close.emit()

    def create_control_buttons(self):
        control_lt = QHBoxLayout()

        btn_save = QPushButton('Сохранить')
        btn_save.clicked.connect(self.save)
        control_lt.addWidget(btn_save, 0, Qt.AlignCenter)

        btn_cancel = QPushButton('Отменить')
        control_lt.addWidget(btn_cancel, 0, Qt.AlignCenter)

        btn_remove = QPushButton('Удалить')
        control_lt.addWidget(btn_remove, 1, Qt.AlignRight)

        return control_lt

    def create_main_form(self):
        fm = QFormLayout()

        fm.addRow(self.header)
        fm.addRow(QLabel(''))

        fm.addRow(self.desk)
        fm.addRow(QLabel(''))

        fm.addRow(QLabel('Когда это нужно сделать?'))
        fm.addRow(self.create_date())
        fm.addRow(self.create_date_buttons())
        fm.addRow(QLabel(''))

        fm.addRow(QLabel('Во сколько?'))
        fm.addRow(self.create_time_choice())

        return fm

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addLayout(self.create_main_form())
        layout.addStretch()
        layout.addLayout(self.create_control_buttons())
        self.setLayout(layout)
