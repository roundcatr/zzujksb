#!/usr/bin/env python3
# coding=utf-8

import os
import json

def userFile():  # 获取配置文件名
    userlist = os.listdir('./.users-pending')
    if userlist == []:  # 已清空
        return ''
    elif userlist[0].startswith('.') or not userlist[0].endswith('.json'):
        os.remove('./.users-pending/'+userlist[0])  # 删除无效文件
        return userFile()
    else:
        return userlist[0]

def getInfo():  # 获取用户信息字典及对应文件名
    userfilename = userFile()
    if userfilename == '':
        return {}, userfilename
    userjson = open('./.users-pending/'+userfilename, encoding='utf-8')
    user = json.load(userjson)
    userjson.close()
    return user, userfilename

def setCookie(userlink, cookie):
    userjson = open('./.users-pending/'+userlink, encoding='utf-8')
    user = json.load(userjson)
    userjson.close()
    user['cookie'] = cookie
    userfilename = os.readlink('./.users-pending/'+userlink)
    userjson = open('./.users-pending/'+userfilename, mode='w', encoding='utf-8')
    json.dump(user, userjson, ensure_ascii=False)
    userjson.close()
