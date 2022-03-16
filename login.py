#!/usr/bin/env python3

import requests

def cutOutId(response):  # 从响应体中截取ptopid和sid两个参数
    pos_ptopid = response.text.find('ptopid=s')
    pos_sid = response.text.find('&sid=')
    if pos_ptopid == -1:
        return '', ''
    ptopid = response.text[pos_ptopid+7:pos_sid]	#ptopid为认证登录信息的关键参数
    sid = response.text[pos_sid+5:pos_sid+23]
    return ptopid, sid

def loginByUserPwd(user):  # 用户名密码登录，同时修改cookie
    headers_mobile = {
	    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
	    'Accept-Encoding': 'gzip, deflate',
	    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/98.0  Mobile/15E148 Safari/605.1.15',
	    'Accept-Language': 'zh-CN,zh;q=0.9',
	    'Referer': 'https://jksb.v.zzu.edu.cn/',
        'Connection': 'close'
    }
    cookie = requests.get("https://jksb.v.zzu.edu.cn:443/vls6sss/zzujksb.dll/first0",headers=headers_mobile).headers.get("Set-Cookie").split(";")[0]
    headers_newCookie = {
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
    pwdLogin_data = {
	    'uid': user['username'],
	    'upw': user['password'],
	    'smbtn': '进入健康状况上报平台',
	    'hh28': '540'  # 此参数会变化且作用不明，不影响使用
    }
    pwdLogin_response = requests.post("https://jksb.v.zzu.edu.cn:443/vls6sss/zzujksb.dll/login", headers=headers_newCookie, data=pwdLogin_data)
    ptopid, sid = cutOutId(pwdLogin_response)
    if ptopid != '':
        user['cookie'] = cookie
    else:
        user['cookie'] = ''
    return ptopid, sid

def getId(user):
    if user['cookie'] == '':
        return loginByUserPwd(user)
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
        ptopid, sid = cutOutId(cookieLogin_response)
        if ptopid != '':
            return ptopid, sid
        else:
            return loginByUserPwd(user)