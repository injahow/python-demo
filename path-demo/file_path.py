#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
 
def load_file():
    # 当前文件路径
    current_path = os.path.abspath(__file__)
    # 当前文件的父目录
    father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep)

    print('\n当前目录:' + current_path)
    print('\n当前父目录:' + father_path)

load_file()