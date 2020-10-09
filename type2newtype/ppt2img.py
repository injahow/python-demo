# -*- coding: UTF-8 -*-

import win32com
import win32com.client
import sys
import os
import math
import urllib

from PIL import Image

def pngMontage(jpg_root, dirName):  
    #打开目录下所有的png图片
    imageList = [Image.open(jpg_root+dirName+'/'+img) for img in os.listdir(jpg_root+dirName) if img.endswith('.JPG')]
    #获取每张图的宽高
    width,height = imageList[0].size
    #新建空白图片并设置图片的宽高,其中高度为所有图片高的总和
    imageList_num = len(imageList)
    
    # longImage = Image.new(imageList[0].mode,(width,(len(imageList)*height)))
    hangshu = math.ceil( (imageList_num-1) / 4 ) #下方行数
    height_min = height//4
    width_min = width//4
    longImage = Image.new(imageList[0].mode, (width, height + hangshu*height_min ), (255,255,255))
    longImage2 = Image.new(imageList[0].mode, (width, height), (255,255,255))

    for index,image in enumerate(imageList):
        img_index = index + 3
        if (img_index == 3 ):
            longImage.paste(image,box=(0,index*height))
            longImage2.paste(image,box=(0,index*height))
        else:
            new_image = image.resize((width_min,height_min),Image.BILINEAR)  # 等比缩放
            longImage.paste(new_image, box=( (img_index % 4)*width_min, height + ((img_index // 4 )- 1)*height_min)) #把小图依次粘贴到新建的空白图片中，其中box是图片位置坐标

    longImage.save(jpg_root + dirName + '-' + 'long.jpg')
    longImage2.save(jpg_root + dirName + '-' + 'cover.jpg')

def ppt2img(ppt_path):
    ppt_root = jpg_root = ppt_path[:ppt_path.rfind('/')] + '/'
    pptFileName = ppt_path[ppt_path.rfind('/') - len(ppt_path)+1:]
    print(ppt_root,'------',pptFileName) 
    powerpoint = win32com.client.Dispatch('Powerpoint.Application')
    #是否后台运行
    #powerpoint.Visible = 1

    ppt = powerpoint.Presentations.Open(ppt_path, ReadOnly=1, Untitled=0, WithWindow=0)
    #保存为图片
    ppt.SaveAs('D:\\' + pptFileName.rsplit('.')[0], 17) # formatType = 17 ppt转图片
    # 关闭打开的ppt文件
    #ppt.Close()
    powerpoint.Quit()
    pngMontage('D:\\', pptFileName[0:-5]) #所有图片拼接成长图

def getlist(floder):
    if os.path.isfile(floder) and floder.endswith('.pptx'):
        ppt2img(floder)
        print (floder+'处理完成')
    else:
        flist = os.listdir(floder)
        for f in flist:
            if os.path.isfile(floder+'/'+f):
                if f.endswith('.pptx'):
                    #处理
                    print ('处理'+floder+'/'+f)
                    ppt2img(floder+'/'+f)
            else:
                print ('遍历子目录 '+str(f))
                getlist(floder+'/'+f)

if __name__ == '__main__':
    getlist('D:/test')