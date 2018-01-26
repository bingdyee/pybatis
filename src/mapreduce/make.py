# -*- coding:utf-8 -*-
import os
from tools.common import list_files


def compile_java():
    files = list_files('java/lib')
    jars = ';'.join(f for f in files)
    cmd = 'javac -cp %s -d java/classes/ java/stock/*.java' % jars
    print(cmd)
    os.system(cmd)


def pack_jar():
    os.chdir('java/classes')
    cmd = 'jar cvfm stock-share.jar manifest.mf stock/*'
    os.system(cmd)


def do_it():
    compile_java()
    pack_jar()

