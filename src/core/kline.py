# -*-coding:utf-8-*-
import datetime
import time
import matplotlib.dates as mpd



def date2num(sdate):
    tm = time.strptime(sdate, "%Y-%m-%d")
    year, month, day = tm[0:3]
    dt = datetime.date(year, month, day)
    num = mpd.date2num(dt)
    return num


def gain_quotes(prices):
    pr = []
    data = []
    for i in range(0, len(prices), 11):
        pr.extend([[
            date2num(prices[i])
            , float(prices[i + 1])
            , float(prices[i + 2])
            , float(prices[i + 3])
            , float(prices[i + 4])
            , float(prices[i + 8])]]
        )
        data.append([prices[i], float(prices[i + 4])])
    return pr, data

def draw_k_line(data):
    pass

