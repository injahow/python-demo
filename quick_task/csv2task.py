#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import datetime
import win32clipboard as wincb

msg_data = {
    '1': ['''xxxx''',
          '''xxxx''',
          '''xxxx'''
          ],
    '2': [
        '''xxxx''',
        '''xxxx''',
        '''xxxx''',
        '''xxxx'''
    ],
    '3': [
        '''xxxx''',
        '''xxxx''',
        '''xxxx'''
    ],
    '4': [
        '''xxxx''',
        '''xxxx''',
        '''xxxx'''
    ],
    '5': [
        '''xxxx''',
        '''xxxx''',
        '''xxxx'''
    ],
    '6': [
        '''xxxx''',
        '''xxxx''',
        '''xxxx'''
    ],
    '7': [
        '''xxxx''',
        '''xxxx''',
        '''xxxx'''
    ]
}


def csv2dict(csv_file):
    output = []
    with open(csv_file, 'r', encoding='utf-8-sig') as cf:
        dict_reader = csv.DictReader(cf)  # [{},{},{}...] 有序字典
        for row in dict_reader:
            d = {}
            for k, v in row.items():
                d[k] = v
            output.append(d)
    return output


def dict2csv(dict_data, csv_file, fieldnames):
    with open(csv_file, 'w', encoding='utf-8-sig') as cf:
        cr = csv.DictWriter(cf, fieldnames=fieldnames)
        cr.writeheader()  # 写入表头
        cr.writerows(dict_data)  # 一次性写入数据
    return


def dictSort(data):
    data.sort(key=lambda obj: obj['msg_index'], reverse=False)  # 由小到大,升序输出
    return data


def setText(aString):  # 写入剪切板
    wincb.OpenClipboard()
    wincb.EmptyClipboard()
    wincb.SetClipboardText(aString)
    wincb.CloseClipboard()


old_csv_obj = csv2dict(
    f'users_{ str(datetime.date.today().strftime("%Y_%m_%d")) }.csv')

old_csv_obj = dictSort(old_csv_obj)
new_csv_obj = old_csv_obj

output_csv = [[], [], [], []]

for i, x in enumerate(old_csv_obj):
    name = x['name']
    name_1 = name[0:1]
    msg_index = x['msg_index']

    if str(int(msg_index) + 1) in msg_data.keys():
        next_index = str(int(msg_index) + 1)
        new_csv_obj[i]['msg_index'] = next_index
    else:
        new_csv_obj[i]['state'] = 'done'
        continue

    next_msg_array = msg_data[next_index]
    next_msg_array = [i.replace('xxxx', name_1) for i in next_msg_array]

    for i, y in enumerate(next_msg_array):
        if i == 0:
            output_csv[0].append({'name': name, 'next_msg': y})
        if i == 1:
            output_csv[1].append({'name': name, 'next_msg': y})
        if i == 2:
            output_csv[2].append({'name': name, 'next_msg': y})
        if i == 3:
            output_csv[3].append({'name': name, 'next_msg': y})

tomorrow = datetime.date.today() + datetime.timedelta(days=1)
fieldnames = ['name', 'state', 'add_time', 'msg_index']
dict2csv(new_csv_obj, f'users_{ str(tomorrow.strftime("%Y_%m_%d")) }.csv', fieldnames)

file_name = [f'output_{i}_' + str(datetime.date.today().strftime("%Y_%m_%d")) + '.csv'
             for i in ['早上', '中午', '下午', '晚上']]

# 保存导出的消息记录
for file_i, output_i in zip(file_name, output_csv):
    fieldnames = ['name', 'next_msg']
    dict2csv(output_i, file_i, fieldnames)

# 根据提示自动复制剪贴板
my_time_i = int(input('|1->早上|2->中午|3->下午|4->晚上|\n')) % 4
my_time = ['早上', '中午', '下午', '晚上'][my_time_i-1]
print(f'当前选择的发送消息时间为:{my_time}!!!')
output = csv2dict(f'output_{my_time}_' + str(datetime.date.today().strftime("%Y_%m_%d")) + '.csv')

for i in output:
    print('姓名:\n' + i['name'] + '\n')
    #print('应发消息:' + i['next_msg'])
    setText(i['next_msg'])
    print('应发消息已经复制到剪贴板!!!')
    x = input('按回车(Enter)键继续......\n\n')
