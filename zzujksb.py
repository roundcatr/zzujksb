#!/usr/bin/env python3

import requests
import json
import os
import sys

os.chdir(sys.path[0])  #切换至当前路径

#判断是否已打卡
statusfile = open('status')
flag = statusfile.read()
statusfile.close()
if flag == 'submitted':
	print('今日已打卡')
	exit()

#读取 json
configfile = open('userinfo.json', encoding='utf-8')
userinfo = json.load(configfile)
configfile.close()

#构造请求头部信息
headers0 = {
	'Connection': 'close',
	'Cache-Control': 'max-age=0',
	'sec-ch-ua': '";Not A Brand";v="99", "Chromium";v="88"',
	'sec-ch-ua-mobile': '?0',
	'Upgrade-Insecure-Requests': '1',
	'Origin': 'https://jksb.v.zzu.edu.cn',
	'Content-Type': 'application/x-www-form-urlencoded',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
	'Sec-Fetch-Site': 'same-origin',
	'Sec-Fetch-Mode': 'navigate',
	'Sec-Fetch-User': '?1',
	'Sec-Fetch-Dest': 'iframe',
	'Referer': 'https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/',	#后续不同请求仅此处有不同
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'zh-CN,zh;q=0.9'
}

print('[用户'+userinfo['用户号']+']')

#登录并获取ID
login_headers = headers0
login_headers['Referer'] += 'first0'	#修改Referer
login_data = {
	'uid': userinfo['用户号'],
	'upw': userinfo['密码'],
	'smbtn': '进入健康状况上报平台',
	'hh28': '754'	#此参数作用未知
}
login_response = requests.post('https://jksb.v.zzu.edu.cn:443/vls6sss/zzujksb.dll/login', headers=login_headers, data=login_data)
pos1 = login_response.text.find('ptopid=s')
pos2 = login_response.text.find('&sid=')
if pos1 == -1:	#无法获取ptopid
	raise Exception('登录失败')
	#抛出异常并退出
print('登录成功')
ptopid = login_response.text[pos1+7:pos2]	#ptopid为认证登录信息的关键参数
sid = login_response.text[pos2+5:pos2+23]	#从响应中截取ptopid与sid两个参数

#请求填报页面
requestform_headers = headers0
requestform_headers['Referer'] += 'jksb?ptopid=' + ptopid + '&sid=' + sid + '&fun2='
requestform_data = {
	'day6': 'b',
	'did': '1',
	'door': '',
	'men6': 'a',	#以上参数作用不明
	'ptopid': ptopid,
	'sid': sid
}
requests.post('https://jksb.v.zzu.edu.cn:443/vls6sss/zzujksb.dll/jksb', headers=requestform_headers, data=requestform_data)

#提交填报结果
submit_headers = headers0
submit_headers['Referer'] += 'jksb'
submit_data = {
	'myvs_1': userinfo['发热'],
	'myvs_2': userinfo['咳嗽'],
	'myvs_3': userinfo['乏力或轻微乏力'],
	'myvs_4': userinfo['鼻塞、流涕、咽痛或腹泻'],
	'myvs_5': userinfo['确诊'],
	'myvs_6': userinfo['疑似'],
	'myvs_7': userinfo['密切接触者'],
	'myvs_8': userinfo['在医疗机构隔离'],
	'myvs_9': userinfo['在集中隔离点隔离'],
	'myvs_10': userinfo['居家隔离'],
	'myvs_11': userinfo['所在小区（村）确诊'],
	'myvs_12': userinfo['共同居住人确诊'],
	'myvs_13': userinfo['健康码颜色'],
	'myvs_13a': userinfo['省份代码'],
	'myvs_13b': userinfo['地市代码'],
	'myvs_13c': userinfo['详细地址'],
	'myvs_24': userinfo['当日返郑'],
	'myvs_26': userinfo['疫苗接种'],
	'memo22': '无法获取',	#如需精确填报时的地理位置可以修改此处为'成功获取'
	'did': '2',
	'door': '',
	'day6': 'b',
	'men6': 'a',
	'sheng6': '',
	'shi6': '',
	'fun3': '',
	'jingdu': '0.0000',	#此处经纬度可一并修改
	'weidu': '0.0000',
	'ptopid': ptopid,
	'sid': sid
}
submit_response = requests.post('https://jksb.v.zzu.edu.cn:443/vls6sss/zzujksb.dll/jksb', headers=submit_headers, data=submit_data)

#判断是否成功
if submit_response.text.find('zzujksb.dll/endok') != -1:	#判断返回结果是否包含填报成功返回页
	statusfile = open('status', mode='w')
	statusfile.write('submitted')
	statusfile.close() #写入status文件
	#print('填报成功')
else:
	raise Exception('发生未知错误，填报失败，请手动检查')
