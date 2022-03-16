#!/usr/bin/env python3

import os
import sys
from userinfo import getInfo, setCookie
from login import getId
from submit import submitInfo
from barkpush import barkPush

os.chdir(sys.path[0])  #切换至当前路径
user, userlink = getInfo()
if user == {}:
	sys.exit()
current_cookie = user['cookie']
ptopid, sid = getId(user)
if user['cookie'] == '':
	barkPush(title='登录失败，请检查用户信息', body='用户'+user['username'], device_key=user['barkid'], level='active', group='健康打卡状态')
	os.remove('./.users-pending/'+userlink)
	sys.exit()
if current_cookie != user['cookie']:
	setCookie(userlink, user['cookie'])
if submitInfo(user, ptopid, sid):
	barkPush(title='打卡成功', body='用户'+user['username'], device_key=user['barkid'], level='passive', group='健康打卡状态')
else:
	barkPush(title='自动打卡失败，请手动上报', body='用户'+user['username'], device_key=user['barkid'], level='active', group='健康打卡状态')
os.remove('./.users-pending/'+userlink)