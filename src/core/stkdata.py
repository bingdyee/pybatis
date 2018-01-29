# -*- coding:utf -8-*-
import tushare as ts
import datetime
import time
import matplotlib as mpl
import matplotlib.dates as mpd
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
from orm.dbutil import DBUtils


mpl.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
mpl.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


class StockRepository:

    BASE_INFO = ['name', 'industry']
    K_QUOTES = ['date', 'open', 'high', 'low', 'close']
    MA = ['ma5', 'ma10', 'ma20']
    DATE_T_FORMAT = '%Y-%m-%d'

    def __init__(self, path):
        self.dbutil = DBUtils()
        self.dbutil.set_instance(path)

    def _date2num(self, sdate):
        tm = time.strptime(sdate, self.DATE_T_FORMAT)
        year, month, day = tm[0:3]
        dt = datetime.date(year, month, day)
        num = mpd.date2num(dt)
        return num

    def _get_quotes(self, arr_data):
        pr = []
        dates = []
        for data in arr_data:
            dates.append(self._date2num(data[0]))
            pr.extend([[
                self._date2num(data[0]),
                float(data[1]),
                float(data[2]),
                float(data[3]),
                float(data[4]),
            ]])
        return pr, dates

    def get_his_data(self, code=None, start='', end='', ktype='D',
                     autype='qfq', index=False, retry_count=3, pause=0.001):
        """
        获取历史数据(日K线)
        """
        data = ts.get_k_data(code=code, start=start, end=end, ktype=ktype, retry_count=retry_count, pause=pause,
                             index=index, autype=autype)
        arr_data = []
        for index, row in data.iterrows():
            dt = []
            for col_name in self.K_QUOTES:
                dt.append(row[col_name])
            arr_data.append(dt)
        return self._get_quotes(arr_data)

    def init_stock_basics(self):
        """
        获取基础股票信息
        """
        data = ts.get_stock_basics()
        for index, row in data.iterrows():
            dt = (index, str(row[self.BASE_INFO[0]]), row[self.BASE_INFO[1]])
            self.dbutil.insert('insert into stock_basics(stock_code, stock_name, stock_industry) values(?, ?, ?)', dt)

    def get_kline_data(self, code, start, end):
        data = ts.get_hist_data(code=code, start=start, end=end)
        ma5, ma10, ma20, arr_data, volumes = [], [], [], [], []
        for index, row in data.iterrows():
            dt = []
            for col_name in self.K_QUOTES:
                if col_name == 'date':
                    dt.append(row.name)
                else:
                    dt.append(row[col_name])
            volumes.append(row['volume'])
            arr_data.append(dt)
            ma5.append(row['ma5'])
            ma10.append(row['ma10'])
            ma20.append(row['ma20'])
        quotes, dates = self._get_quotes(arr_data)
        return {'code': code, 'dates': dates, 'quotes': quotes,
                'volumes': volumes, 'ma5': ma5, 'ma10': ma10, 'ma20': ma20}

    def get_time_data(self, code):
        data = ts.get_today_ticks(code)
        return data

    def get_volume_data(self):
        pass


query = {'code': '300355', 'start': '2017-10-09', 'end': '2017-10-12'}


def draw_kline_test(query):
    repos = StockRepository('../../resources/base_info')
    data = repos.get_kline_data(**query)
    db = DBUtils()
    db.set_instance('../../resources/base_info')
    title = db.select('select stock_name from stock_basics where stock_code='+data['code'])
    fig, ax = plt.subplots(figsize=(26, 12))
    ax.xaxis.set_major_formatter(mpd.DateFormatter('%Y-%m-%d'))
    mpf.candlestick_ohlc(ax, data['quotes'], width=0.5, colorup='r', colordown='g')
    title = u'%s日K线' % title[0][0].decode('utf-8')
    plt.plot(data['dates'], data['ma5'], 'b-', color='r', label='$MA5$')
    plt.plot(data['dates'], data['ma10'], 'b-', color='b', label='$MA10$')
    plt.plot(data['dates'], data['ma20'], 'b-', color='g', label='$MA20$')
    plt.title(title)
    plt.ylabel(u'股价(元)')
    plt.xlabel(u'日期')
    plt.legend(loc='best')
    plt.show()


def test():
    repos = StockRepository('../../resources/base_info')
    data = repos.get_time_data(query['code'])
    for index, row in data.iterrows():
        print(row['time'], row['price'])


