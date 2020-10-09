#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
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
    ],

}


def dictSort(data):
    data.sort(key=lambda obj: obj['msg_index'], reverse=False)  # 由小到大,升序输出
    return data


def setText(aString):  # 写入剪切板
    wincb.OpenClipboard()
    wincb.EmptyClipboard()
    wincb.SetClipboardText(aString)
    wincb.CloseClipboard()


f_old = open(
    f'users_{ str(str(datetime.date.today().strftime("%Y_%m_%d"))) }.json', 'r', encoding='utf-8')
old_json_str = f_old.read()
old_json_obj = json.loads(old_json_str)

old_json_obj = dictSort(old_json_obj)
new_json_obj = old_json_obj

output_json = [[], [], [], []]

for i, x in enumerate(old_json_obj):
    name = x['name']
    name_1 = name[0:1]
    msg_index = x['msg_index']

    if str(int(msg_index) + 1) in msg_data.keys():
        next_index = str(int(msg_index) + 1)
        new_json_obj[i]['msg_index'] = next_index
    else:
        new_json_obj[i]['state'] = 'done'
        continue

    next_msg_array = msg_data[next_index]
    next_msg_array = [i.replace('xxxx', name_1) for i in next_msg_array]

    for i, y in enumerate(next_msg_array):
        if i == 0:
            output_json[0].append({'name': name, 'next_msg': y})
        if i == 1:
            output_json[1].append({'name': name, 'next_msg': y})
        if i == 2:
            output_json[2].append({'name': name, 'next_msg': y})
        if i == 3:
            output_json[3].append({'name': name, 'next_msg': y})

f_old.close()
tomorrow = datetime.date.today() + datetime.timedelta(days=1)
with open(f'users_{ str(tomorrow.strftime("%Y_%m_%d")) }.json', 'w+', encoding='utf-8') as f2:
    f2.write(json.dumps(new_json_obj))

file_name = [f'output_{i}_' + str(datetime.date.today().strftime("%Y_%m_%d")) + '.json'
             for i in ['早上', '中午', '下午', '晚上']]

# 保存导出的消息记录
for file_p, output_i in zip(file_name, output_json):
    with open(file_p, 'w+', encoding='utf-8') as out_f:
        out_f.write(json.dumps(output_i))

# 根据提示自动复制剪贴板
my_time_i = int(input('|1->早上|2->中午|3->下午|4->晚上|\n')) % 4
my_time = ['早上', '中午', '下午', '晚上'][my_time_i-1]
print(f'当前选择的发送消息时间为:{my_time}!!!')

with open(f'output_{my_time}_' + str(datetime.date.today().strftime("%Y_%m_%d")) + '.json', 'r', encoding='utf-8') as input_f:
    output = json.loads(input_f.read())

for i in output:
    print('姓名:\n' + i['name'] + '\n')
    #print('应发消息:' + i['next_msg'])
    setText(i['next_msg'])
    print('应发消息已经复制到剪贴板!!!')
    x = input('按回车(Enter)键继续......\n\n')
