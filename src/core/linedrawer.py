# -*- coding:utf-8 -*-
import sys
from PyQt5 import QtWidgets
import matplotlib.dates as mpd
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from .stkdata import StockRepository
from tools.dbutil import DBUtils


class Figure_Canvas(FigureCanvas):
    def __init__(self, parent=None, path='../../resources/base_info', width=11, height=5, dpi=100):
        fig, ax = plt.subplots(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)
        self.repository = StockRepository(path)
        self.database = DBUtils(path)
        self.setParent(parent)
        self.axes = ax

    def draw_k_line(self, code='300355', start='2017-10-09', end='2017-10-12'):
        data = self.repository.get_kline_data(code=code, start=start, end=end)
        title = self.database.select('select stock_name from stock_basics where stock_code='+data['code'])
        self.axes.xaxis.set_major_formatter(mpd.DateFormatter('%Y-%m-%d'))
        mpf.candlestick_ohlc(self.axes, data['quotes'], width=0.5, colorup='r', colordown='g')
        title = u'%s日K线' % title[0][0].decode('utf-8')
        self.axes.plot(data['dates'], data['ma5'], 'b-', color='r', label='$MA5$')
        self.axes.plot(data['dates'], data['ma10'], 'b-', color='b', label='$MA10$')
        self.axes.plot(data['dates'], data['ma20'], 'b-', color='g', label='$MA20$')
        self.axes.set_title(title)
        self.axes.set_ylabel(u'股价(元)')
        self.axes.set_xlabel(u'日期')
        self.axes.legend(loc='best')

    def draw_time_line(self):
        pass

    def draw_volume_line(self):
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    figure = Figure_Canvas()
    figure.draw_k_line()
    figure.show()
    sys.exit(app.exec_())
