import sys

from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QStackedWidget, QApplication, QMainWindow

from task_list import TaskList
from task_view import TaskView
from tasks.model import TaskModel


class Root(QMainWindow):
    task_list_index = 0
    task_view_index = 1

    def __init__(self):
        super().__init__()
        self.task_view = None
        self.task_list = None
        self.model = None
        self.initUI()

    def initUI(self):
        # self.cal = QCalendarWidget(self)
        # self.cal.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        # self.cal.setGeometry(0, 0, 250, 250)

        self.model = TaskModel()
        self.central = QStackedWidget()

        self.task_list = TaskList(self.model)
        self.task_list.open.connect(self.task_open)
        self.central.insertWidget(Root.task_list_index, self.task_list)

        self.task_view = TaskView(self.model)
        self.task_view.close.connect(self.task_view_close)
        self.central.insertWidget(Root.task_view_index, self.task_view)

        self.central.setCurrentIndex(Root.task_list_index)
        self.setCentralWidget(self.central)

        # QDialog flags:
        #   Qt.Dialog |
        #   Qt.WindowTitleHint |
        #   Qt.WindowSystemMenuHint |
        #   Qt.WindowContextHelpButtonHint |
        #   Qt.WindowCloseButtonHint
        self.setWindowFlags(Qt.Dialog | Qt.WindowStaysOnTopHint)
        self.setGeometry(700, 300, 250, 300)
        self.setWindowTitle('Calendar')

    @pyqtSlot(int)
    def task_open(self, index):
        self.task_view.set_task(index)
        self.central.setCurrentIndex(Root.task_view_index)

    @pyqtSlot()
    def task_view_close(self):
        self.central.setCurrentIndex(Root.task_list_index)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        # "motif", "Windows", "cde", "Plastique", "Cleanlooks", "windowsvista"
        # app.setStyle(QStyleFactory.create('Plastique'))
        ex = Root()
        ex.show()
        sys.exit(app.exec_())
    except Exception as e:
        print('Error exit' + str(e))
