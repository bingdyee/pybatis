# -*- coding:utf -8-*-
import pandas as pd
import multiprocessing as mp
import tushare as ts
from mapper.stock_info import StockInfoMappper
from tools.common import list_files


class DataRepository:

    CPU_NUM = 2

    def __init__(self, path):
        self.files = list_files(path)

    @staticmethod
    def init_basics_info():
        data = ts.get_stock_basics()
        for index, row in data.iterrows():
            dt = (index, str(row['name']), row['industry'])
            StockInfoMappper.insert_stock_info(data=dt)

    def data2db_job(self, scope):
        for index in range(scope[0], scope[1]):
            print("插入:%s开始" % self.files[index])
            pd.read_csv(self.files[index])
            StockInfoMappper.insert_stock_info()
            print("插入:%s接受" % self.files[index])

    def start_job(self):
        total = len(self.files)
        pool = mp.Pool(processes=self.CPU_NUM)
        pool.apply_async(self.data2db_job, [0, total/2])
        pool.apply_async(self.data2db_job, [total/2 + 1, total - 1])
        pool.close()
        pool.join()


