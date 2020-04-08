# -*- coding:utf-8 -*-
import xml.sax as dom
from dbutil import DBUtils
from utils import Singleton


class MapperHandler(dom.ContentHandler):

    def __init__(self):
        super(MapperHandler, self).__init__()
        self.CurrentData = ""
        self.CurrentId = ""
        self.CurrentSql = ""
        self.m_str_sql = {}

    def startElement(self, tag, attributes):
        """
        Event of start element
        """
        self.CurrentData = tag
        if attributes.get('id'):
            self.CurrentId = attributes["id"]
            self.CurrentSql = ""

    def endElement(self, tag):
        """
        Event of end element
        """
        if self.CurrentId:
            if self.m_str_sql.get(self.CurrentId):
                raise Exception("Existence of the same name method:%s" % self.CurrentId)
            self.m_str_sql[self.CurrentId] = self.CurrentSql
        self.CurrentData = ""
        self.CurrentId = ""
        self.CurrentSql = ""

    def characters(self, content):
        """
        Event of content
        """
        if content.strip():
            self.CurrentSql += content.strip()


@Singleton
class Mapper:

    def __init__(self, db_path, xmls):
        self.parser = dom.make_parser()
        self.parser.setFeature(dom.handler.feature_namespaces, 0)
        self.handler = MapperHandler()
        self.parser.setContentHandler(self.handler)
        self.dbutil = DBUtils()
        self.dbutil.set_instance(db_path)
        self.resolve(xmls)

    def resolve(self, path):
        for _ in path:
            self.parser.parse(_)

    def exec(self, sql, data=None):
        return self.dbutil.execute(sql, data)

    def __getitem__(self, item):
        return self.handler.m_str_sql.get(item)


m = Mapper('../../resources/stock.db3',
           ["../../resources/mapper/stock_info.xml",
            "../../resources/mapper/stock_map.xml"])


def mapper(func):

    global m

    def _invoke(**kw):
        sql = m[func.__name__]
        data = kw['data'] if kw.get('data') else None
        return m.exec(sql, data)

    return _invoke
