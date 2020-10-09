#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
#import time

with open('D:/test.csv', 'r') as f:
    all_strs = f.read()
    one_strs = all_strs.split('\n') #全部数据

output_data = []
_id = 0
for line in lines:
    _id += 1
    line_arr = line.split(',')
    #print(name_msg_str)
    name = line_arr[0]
    msg = line_arr[1]

    json_one = {
        'id': _id,
        'title' : name,
        'content' : msg
    }
    output_data.append(json_one)

with open('D:/test.json', 'w') as f2:
    f2.write(json.dumps(output_data))

