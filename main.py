import sys

from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QWidget

from task_list import TaskList
from model import Task
from task_view import TaskView


class Root(QMainWindow):
    def __init__(self):
        super().__init__()
        self.task_view = TaskView()
        self.task_list = TaskList()
        self.initUI()

    def initUI(self):
        # self.cal = QCalendarWidget(self)
        # self.cal.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        # self.cal.setGeometry(0, 0, 250, 250)

        self.task_list.open.connect(self.task_open)
        self.setCentralWidget(self.task_list)

        # QDialog flags:
        #   Qt.Dialog |
        #   Qt.WindowTitleHint |
        #   Qt.WindowSystemMenuHint |
        #   Qt.WindowContextHelpButtonHint |
        #   Qt.WindowCloseButtonHint
        self.setWindowFlags(Qt.Dialog | Qt.WindowStaysOnTopHint)
        self.setGeometry(700, 300, 250, 300)
        self.setWindowTitle('Calendar')

    @pyqtSlot(Task)
    def task_open(self, task):
        self.task_view.set_task(task)
        w = QWidget()
        w.setLayout(self.task_view)
        self.setCentralWidget(w)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # "motif", "Windows", "cde", "Plastique", "Cleanlooks", "windowsvista"
    # app.setStyle(QStyleFactory.create('Plastique'))
    ex = Root()
    ex.show()
    sys.exit(app.exec_())
