#!/usr/bin/env python3

import requests

def submitInfo(user, ptopid, sid):
    headers_submit = {
        'Cookie': user['cookie'],
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://jksb.v.zzu.edu.cn',
        'Content-Length': '558',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Mobile/15E148 Safari/604.1',
        'Referer': 'https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/jksb',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'close'
    }
    data_submit = {
        'myvs_1': '否',
        'myvs_2': '否',
        'myvs_3': '否',
        'myvs_4': '否',
        'myvs_5': '否',
        'myvs_6': '否',
        'myvs_7': '否',
        'myvs_8': '否',
        'myvs_9': '否',
        'myvs_10': '否',
        'myvs_11': '否',
        'myvs_12': '否',
        'myvs_13': 'g',
        'myvs_13a': user['city'][0:2],
        'myvs_13b': user['city'],
        'myvs_13c': user['address'],
        'myvs_24': '否',
        'myvs_26': user['vaccine'],
        'memo22': '成功获取',
        'did': '2',
        'door': '',
        'day6': '',
        'men6': 'a',
        'sheng6': '',
        'shi6': '',
        'fun3': '',
        'jingdu': user['longitude'],
        'weidu': user['latitude'],
        'ptopid': ptopid,
        'sid': sid
    }
    response_submit = requests.post("https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/jksb", headers=headers_submit, data=data_submit)
    if response_submit.text.find("zzujksb.dll/endok") != -1:
        return True
    else:
        return False