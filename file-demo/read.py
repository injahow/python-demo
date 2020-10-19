#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

"""
1、读取文件的三个方法：read()、readline()、readlines()
2、三个方法均可接受一个变量用以限制每次读取的数据量，通常不使用该变量。
"""

"""
关于read()方法：
1、读取整个文件，将文件内容放到一个字符串变量中
2、如果文件大于可用内存，不可能使用这种处理
"""
'''
file_object = open("test.py",'r') #创建一个文件对象，也是一个可迭代对象
try:
    all_the_text = file_object.read()  #结果为str类型
    print(type(all_the_text))
    print("all_the_text=",all_the_text)
finally:
    file_object.close()
'''
"""
关于readline()方法：
1、readline()每次读取一行，比readlines()慢得多
2、readline()返回的是一个字符串对象，保存当前行的内容
"""'''
file_object1 = open("test.py",'r')
try:
  while True:
      line = file_object1.readline()
      if line:
          print("line=",line)
      else:
          break
finally:
    file_object1.close()
'''
"""
关于readlines()方法：
1、一次性读取整个文件。!!!!!!!
2、自动将文件内容分析成一个行的列表。
"""'''
file_object2 = open("test.py",'r')
try:
  lines = file_object2.readlines()
  print("type(lines)=",type(lines)) #type(lines)= <type 'list'>
  for line in lines:
      print("line=",line)
finally:
    file_object2.close()
'''


f = open('***.ini','r')
try:
    data = f.read()
    #print("type(lines)=",type(lines)) #type(lines)= <type 'list'>

    data_json = json.loads(data)
    if ('7119' in data_json) :
        a = data_json['7119']
        print(a)


finally:
    f.close()
