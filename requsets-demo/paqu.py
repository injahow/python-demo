#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import json

class Spider:
    def __init__(self):
        self.temp_url = 'https://a.com?id={}'

    def parse_url(self, start_url):
        headers = {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
            #'Referer' : '***'
        }
        response = requests.get(start_url, headers=headers, timeout=5)
        return response.content.decode()

    def get_content_list(self, html_str): # 获取json数据
        data_dict = json.loads(html_str)
        content_list = data_dict['data']
        return content_list

    def save_content_list(self, content_list): # 储存
        with open('data.json', 'a', encoding='utf-8') as f:
            for content in content_list:
                f.write(json.dumps(content, ensure_ascii=False)) #,indent=2
                f.write('\n')

    def run(self): # 爬取流程
        num = 1
        total = 100
        while num < total:
            # 1.起始url
            start_url = self.temp_url.format(num)
            # 2.获取源码
            html_str = self.parse_url(start_url)
            # 3.获取数据
            content_list = self.get_content_list(html_str)
            # 4.存储数据
            self.save_content_list(content_list)
            # 5.构造下一个url，循环获取
            num += 1

            print(str(num) + ' is ok!')

if __name__ == '__main__':
    x = Spider()
    x.run()
