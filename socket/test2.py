#!/usr/bin/env python
# -*- coding: utf-8 -*-
# sockdemo.py
#
# test

def outForList(content, row):
    for i in range(row):
        tmp = content[i::row]
        row_content = ''
        for j in tmp:
            row_content += str(j).ljust(15)
        print row_content

outForList([1,2,3,],3)

