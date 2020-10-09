#!/usr/bin/python
# -*- coding: utf-8 -*-

import win32clipboard as w
import win32con

def getText():  # 读取剪切板
    w.OpenClipboard()
    d = w.GetClipboardData(win32con.CF_TEXT)
    w.CloseClipboard()
    return d

def setText(aString):  # 写入剪切板
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardText(aString)
    w.CloseClipboard()

if __name__ == '__main__':
    a = "hello"
    setText(a)
