#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import urllib.request

'''
print("downloading with requests")
url = '' 
r = requests.get(url)
with open("1.jpg", "wb") as code:
    code.write(r.content)
'''

def download_0(url, headers, file_path):
    # 视频分段下载
    req = urllib.request.Request(url, headers=headers)
    r = urllib.request.urlopen(req)
    file_size = int(r.headers.get('Content-Length'))
    print(file_size)
    if file_size % (1024*1024) == 0:
        download_times = file_size//(1024*1024)
    else:
        download_times = file_size//(1024*1024)+1
    i=0
    for x in range(0, download_times):
        req.headers['Range'] = 'bytes=%s-%s' % (i, i+1024*1024)
        with urllib.request.urlopen(req) as response:
            with open(file_path, "ab+") as video:
                video.write(response.read())
        i+=1024*1024

def download(url, headers, file_path):
    status = requests.get(url).status_code
    if (status == 403):
        return ''
    r = urllib.request.Request(url, headers=headers)
    u = urllib.request.urlopen(r)
    with open(file_path, 'wb') as f:
        while True:
            tmp = u.read(1024)
            if not tmp:
                break
            f.write(tmp)

ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
headers = {'User-Agent': ua}
