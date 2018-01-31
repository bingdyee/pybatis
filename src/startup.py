# -*-coding:utf-8-*-
import sys
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from graphics.form_login import Ui_Form


class Figure_Canvas(FigureCanvas):

    def __init__(self, parent=None, width=11, height=5, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        self.axes = fig.add_subplot(111)

    def test(self):
        x = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        y = [23, 21, 32, 13, 3, 132, 13, 3, 1]
        self.axes.plot(x, y)


def mpl_test():
    app = QtWidgets.QApplication(sys.argv)
    fig = Figure_Canvas()
    fig.test()
    fig.show()
    sys.exit(app.exec_())


class MainWindow(QtWidgets.QWidget):

    """
    For Qt Designer's Files
    """

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    # main()
    s = '1 == 1'
    print(eval(s))
