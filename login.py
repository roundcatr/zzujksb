#!/usr/bin/env python3
# coding=utf-8

import requests

def pwdlogin(user):  # 用户名密码登录，同时修改 cookie
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
    pos_ptopid = pwdlogin_response.text.find('ptopid=s')
    pos_sid = pwdlogin_response.text.find('&sid=')
    ptopid = pwdlogin_response.text[pos_ptopid+7:pos_sid]
    sid = pwdlogin_response.text[pos_sid+5:pos_sid+23]
    if ptopid != '':
        user['cookie'] = cookie
    else:
        user['cookie'] = ''
    return ptopid, sid

def getId(user):
    if user['cookie'] == '':
        return pwdlogin(user)
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
    pos_ptopid = cookieLogin_response.text.find('ptopid=s')
    pos_sid = cookieLogin_response.text.find('&sid=')
    ptopid = cookieLogin_response.text[pos_ptopid+7:pos_sid]
    sid = cookieLogin_response.text[pos_sid+5:pos_sid+23]
    if ptopid != '':
        return ptopid, sid
    else:
        return pwdlogin(user)


def submit(user, ptopid, initsid):

    # 第一步：获取初始页面
    headers_initpage = {
        'Cookie': user['cookie'],
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Mobile/15E148 Safari/604.1',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Referer': 'https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/first0',
        'Connection': 'close'
    }
    response_initpage = requests.get("https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/first6?ptopid="+ptopid+"&sid="+initsid+"&fun2=&id8=", headers=headers_initpage)
    
    # 第二步：作用未知
    headers2 = {
        'Cookie': user['cookie'],
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Mobile/15E148 Safari/604.1',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Referer': 'https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/first6?ptopid='+ptopid+'&sid='+initsid+'&fun2=&id8=',
        'Connection': 'close'
    }
    pos_sid = response_initpage.text.find('&sid=', response_initpage.text.find('<iframe name="zzj_fun_426" id="zzj_fun_426s"'))
    sid2 = response_initpage.text[pos_sid+5:pos_sid+23]
    requests.get("https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/getsomething?ptopid="+ptopid+"&sid="+sid2, headers=headers2)
    
    # 第三步：请求信息页面，从中获取用于反脚本的隐藏参数
    headers_infopage = {
        'Cookie': user['cookie'],
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Mobile/15E148 Safari/604.1',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Referer': 'https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/first6?ptopid='+ptopid+'&sid='+initsid+'&fun2=&id8=',
        'Connection': 'close'
    }
    # 从初始页面中截取 sid
    pos_sid = pos_sid = response_initpage.text.find('&sid=', response_initpage.text.find('<iframe name="zzj_top_6s" id="zzj_top_6s"'))
    sid_infopage = response_initpage.text[pos_sid+5:pos_sid+23]
    response_infopage = requests.get("https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/jksb?ptopid="+ptopid+"&sid="+sid_infopage+"&fun2=", headers=headers_infopage)
    # 获取反脚本的隐藏参数
    hiddenkeypos = response_infopage.text.find('type="hidden" name="fun18" value=')+34
    hiddenkey = response_infopage.text[hiddenkeypos:hiddenkeypos+3]

    # 第四步：作用未知
    headers4 = {
        'Cookie': user['cookie'],
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Mobile/15E148 Safari/604.1',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Referer': 'https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/first6?ptopid='+ptopid+'&sid='+sid_infopage+'&fun2=&id8=',
        'Connection': 'close'
    }
    pos_sid = pos_sid = response_infopage.text.find('&sid=', response_infopage.text.find('<iframe name="zzj_fun_426" id="zzj_fun_426s"'))
    sid4 = response_infopage.text[pos_sid+5:pos_sid+23]
    requests.get("https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/getsomething?ptopid="+ptopid+"&sid="+sid4, headers=headers4)

    # 第五步：向服务器请求填报页面，否则打卡无效
    headers_requestform = {
        'Cookie': user['cookie'],
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://jksb.v.zzu.edu.cn',
        'Content-Length': '82',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Mobile/15E148 Safari/604.1',
        'Referer': 'https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/jksb?ptopid='+ptopid+'&sid='+sid_infopage+'&fun2=',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'close'
    }
    pos_sid = pos_sid = response_infopage.text.find('<input type="hidden" name="sid" value=', response_infopage.text.find('<input type="hidden" name="ptopid" value='))+39
    sid_form = response_infopage.text[pos_sid:pos_sid+18]
    data_requestform = {
        'did': '1',
        'door': '',
        'fun18': hiddenkey,
        'men6': 'a',
        'ptopid': ptopid,
        'sid': sid_form
    }
    formpage = requests.post('https://jksb.v.zzu.edu.cn:443/vls6sss/zzujksb.dll/jksb', headers=headers_requestform, data=data_requestform)

    # 第六步：作用未知
    headers6 = {
        'Cookie': user['cookie'],
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Mobile/15E148 Safari/604.1',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Referer': 'https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/jksb',
        'Connection': 'close'
    }
    pos_sid = formpage.text.find('&sid=', response_initpage.text.find('<iframe name="zzj_fun_426" id="zzj_fun_426s"'))
    sid6 = formpage.text[pos_sid+5:pos_sid+23]
    requests.get("https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/getsomething?ptopid="+ptopid+"&sid="+sid6, headers=headers6)

    # 第七步：上报数据
    headers_submit = {
        'Cookie': user['cookie'],
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://jksb.v.zzu.edu.cn',
        'Content-Length': '614',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Mobile/15E148 Safari/604.1',
        'Referer': 'https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/jksb',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'close'
    }
    pos_sid = pos_sid = formpage.text.find('<input type="hidden" name="sid" value=', formpage.text.find('<input type="hidden" name="ptopid" value='))+39
    sid_submit = formpage.text[pos_sid:pos_sid+18]
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
        'fun18': hiddenkey,
        'fun3': '',
        'jingdu': user['longitude'],  # 所在经度坐标
        'weidu': user['latitude'],  # 所在纬度坐标
        'ptopid': ptopid,
        'sid': sid_submit
    }
    response_submit = requests.post("https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/jksb", headers=headers_submit, data=data_submit)

    # 第八步：作用未知
    #pos_sid = response_submit.text.find('&sid=', response_initpage.text.find('<iframe name="zzj_fun_426" id="zzj_fun_426s"'))
    #sid8 = response_submit.text[pos_sid+5:pos_sid+23]
    #requests.get("https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/getsomething?ptopid="+ptopid+"&sid="+sid8, headers=headers6)

    # 判断是否成功
    if response_submit.text.find("/endok?") != -1:
        return True
    else:
        return False