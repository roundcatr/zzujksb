#!/usr/bin/env python3
# coding=utf-8

import requests

def cutId(response):  # 从响应体中截取ptopid和sid两个参数
    pos_ptopid = response.text.find('ptopid=s')
    pos_sid = response.text.find('&sid=')
    if pos_ptopid == -1:
        return '', ''
    ptopid = response.text[pos_ptopid+7:pos_sid]	#ptopid为认证登录信息的关键参数
    sid = response.text[pos_sid+5:pos_sid+23]
    return ptopid, sid

def pwdlogin(user):  # 用户名密码登录，同时修改cookie
    headers_mobile = {
	    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
	    'Accept-Encoding': 'gzip, deflate',
	    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/98.0  Mobile/15E148 Safari/605.1.15',
	    'Accept-Language': 'zh-CN,zh;q=0.9',
	    'Referer': 'https://jksb.v.zzu.edu.cn/',
        'Connection': 'close'
    }
    cookie = requests.get("https://jksb.v.zzu.edu.cn:443/vls6sss/zzujksb.dll/first0",headers=headers_mobile).headers.get("Set-Cookie").split(";")[0]
    headers_newcookie = {
        'Cookie': cookie,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://jksb.v.zzu.edu.cn',
        'Content-Length': '135',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/98.0  Mobile/15E148 Safari/605.1.15',
        'Referer': 'https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/first0',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'close'
    }
    pwdlogin_data = {
	    'uid': user['username'],
	    'upw': user['password'],
	    'smbtn': '进入健康状况上报平台',
	    'hh28': '540'  # 此参数会变化且作用不明，不影响使用
    }
    pwdlogin_response = requests.post("https://jksb.v.zzu.edu.cn:443/vls6sss/zzujksb.dll/login", headers=headers_newcookie, data=pwdlogin_data)
    ptopid, sid = cutId(pwdlogin_response)
    if ptopid != '':
        user['cookie'] = cookie
    else:
        user['cookie'] = ''
    return ptopid, sid

def getId(user):
    if user['cookie'] == '':
        return pwdlogin(user)
    else:
        headers_cookie = {
            'Cookie': user['cookie'],
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/98.0  Mobile/15E148 Safari/605.1.15',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Referer': 'http://jksb.v.zzu.edu.cn/',
            'Connection': 'close'
        }
        cookieLogin_response = requests.get("https://jksb.v.zzu.edu.cn:443/vls6sss/zzujksb.dll/first0", headers=headers_cookie)
        ptopid, sid = cutId(cookieLogin_response)
        if ptopid != '':
            return ptopid, sid
        else:
            return pwdlogin(user)

def submit(user, ptopid, sid):

    # 先向服务器请求填报页面，否则打卡无效
    headers_requestform = {
        'Cookie': user['cookie'],
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://jksb.v.zzu.edu.cn',
        'Content-Length': '82',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Mobile/15E148 Safari/604.1',
        'Referer': 'https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/jksb?ptopid='+ptopid+'&sid='+sid+'&fun2=',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'close'
    }
    data_requestform = {
        'did': '1',
        'door': '',
        'men6': 'a',	#以上参数作用不明
        'ptopid': ptopid,
        'sid': sid
    }
    requests.post('https://jksb.v.zzu.edu.cn:443/vls6sss/zzujksb.dll/jksb', headers=headers_requestform, data=data_requestform)

    # 然后再上报数据
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
        'myvs_1': '否',  # 是否发热
        'myvs_2': '否',  # 是否咳嗽
        'myvs_3': '否',  # 是否乏力
        'myvs_4': '否',  # 是否鼻塞、流涕、咽痛或腹泻
        'myvs_5': '否',  # 是否被确诊
        'myvs_6': '否',  # 是否为疑似
        'myvs_7': '否',  # 是否为密接
        'myvs_8': '否',  # 是否在医院隔离治疗
        'myvs_9': '否',  # 是否被集中隔离
        'myvs_10': '否',  # 是否被居家隔离
        'myvs_11': '否',  # 所在社区是否有确诊
        'myvs_12': '否',  # 共同居住人是否确诊
        'myvs_13': 'g',  # 健康码颜色
        'myvs_13a': user['city'][0:2],  #省份代码（从地市代码中截取）
        'myvs_13b': user['city'],  # 地市代码
        'myvs_13c': user['address'],  # 详细地址
        'myvs_24': '否',  # 是否当日返郑
        'myvs_26': user['vaccine'],  # 疫苗接种情况
        'memo22': '成功获取',  # 位置状态
        'did': '2',
        'door': '',
        'day6': '',
        'men6': 'a',
        'sheng6': '',
        'shi6': '',
        'fun3': '',
        'jingdu': user['longitude'],  # 所在经度坐标
        'weidu': user['latitude'],  # 所在纬度坐标
        'ptopid': ptopid,
        'sid': sid
    }
    response_submit = requests.post("https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/jksb", headers=headers_submit, data=data_submit)

    # 根据响应判断是否成功
    if response_submit.text.find("zzujksb.dll/endok") != -1:
        return True
    else:
        return False