# -*- coding:utf-8 -*-
"""
@File      : parse.py
@Software  : SingularAI
@Time      : 2018/1/29 14:30
@Author    : yubb

<sql id=''>
<include ref="sql"/>
<if/>
<for/>

"""
import re
from xml.dom.minidom import parse, Node
import xml.dom.minidom
from .dbutil import DBUtils
from .model import *


class Constant:
    id = 'id'
    namespace = 'namespace'
    mapper = 'mapper'
    label_sql = 'sql'
    label_where = 'where'
    label_if = 'if'
    label_for = 'for'
    label_include = 'include'
    label_update = 'update'
    label_delete = 'delete'
    label_select = 'select'
    label_insert = 'insert'
    op_label = [label_delete, label_insert, label_select, label_update]


class XmlNode:

    def __init__(self, namespace=None, id=None, op=None, attrs=None, vars=None, data=None):
        self.namespace = namespace
        self.id = id
        self.op = op
        self.attrs = attrs
        self.vars = vars
        self.data = data

    def __str__(self):
        return '[id: %s、op: %s、attrs: %s、vars: %s、 data: %s]' % (self.id, self.op, self.attrs, self.vars, self.data)


class XmlParsingError(Exception):

    def __init__(self, info):
        super(XmlParsingError, self).__init__(info)


class MapperParse:

    def __init__(self, xmls):
        self.xmls = xmls
        self.mappers = {}

    def parse(self):
        for xPath in xmls:
            dom_tree = xml.dom.minidom.parse(xPath)
            root = dom_tree.documentElement

            if root.hasAttribute(Constant.namespace):
                namespace = root.getAttribute(Constant.namespace)
            else:
                raise XmlParsingError('Empty namespace!')

            child_nodes = root.childNodes
            for node in child_nodes:
                xmlNode = XmlNode()
                xmlNode.namespace = namespace
                # select/insert/update/delete
                if node.nodeType == Node.ELEMENT_NODE and node.nodeName in Constant.op_label:
                    xmlNode.op = node.nodeName
                    if not node.hasAttribute(Constant.id):
                        raise XmlParsingError('id is null!')
                    xmlNode.id = node.getAttribute(Constant.id)
                    attrs = node.attributes
                    # parse attrs
                    if attrs:
                        m_attrs = {}
                        for idx in range(attrs.length):
                            if attrs.item(idx).name != Constant.id:
                                m_attrs[attrs.item(idx).name] = attrs.item(idx).value
                        xmlNode.attrs = m_attrs

                    xmlNode.data = node.childNodes
                    self.mappers[xmlNode.namespace + '.' + xmlNode.id] = xmlNode


class EasyDB:

    def __init__(self, path, xmls):
        self.dbutil = DBUtils()
        self.dbutil.set_instance(path)
        self.mp = MapperParse(xmls)
        self.mp.parse()

    def exec(self, sql, data=None):
        return self.dbutil.execute(sql, data)


path = '../../resources/stock.db3'
xmls = ["stock_map.xml"]
db = EasyDB(path, xmls)


def mapper(*args, **kargs):
    global db

    def decorator(func):
        node = db.mp.mappers.get(func.__qualname__)
        if not node:
            raise XmlParsingError('No method mapper: <%s>' % func.__qualname__)

        def _invoke(**margs):
            strSql = ''
            for n in node.data:
                if n.nodeType == Node.TEXT_NODE:
                    data = n.data.strip()
                    if len(data) > 1:
                        strSql += data
            parms = re.findall(r'#{(.+?)}', strSql)
            pas = []
            for p in parms:
                if not margs.get(p.strip()):
                    raise Exception('')
                # prevent SQL injection
                strSql = strSql.replace('#{' + p + '}', "?")
                pas.append(margs.get(p.strip()))
            return db.exec(sql=strSql, data=tuple(pas))

        return _invoke

    return decorator


def test():
    class Mapper:

        @mapper(sql="select * from tb_stock_info")
        def selecTest(**kw): pass

    class Stock(Model):
        id = Int('id')
        code = Varchar('code')

    st = Stock(id=2, code='603161')
    rs = Mapper.selecTest(**st)
    print()
    print("Result: ", rs)
