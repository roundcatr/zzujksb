# 郑州大学健康状况上报平台自动填报脚本

仅用于郑州大学健康状况上报平台。

2022.12.26 更新：结束了，此脚本留作纪念。

## 背景

自 2020 年初疫情发生以来，学校要求师生员工每天通过健康状况上报平台填报健康状况。~~因大多数同学始终在校园内，健康状况极少变化，故编写脚本以实现健康状况无变化时的自动上报。~~

## **注意**

请勿利用此脚本自动化尝试他人用户信息，服务器配置有反暴力破解措施，此脚本不包含识别图片验证码的模块，多次尝试错误信息会导致服务器要求填写图片验证码而无法填报，甚至导致 IP 被服务器拉黑！

<font color = #FF0000>仅用于个人健康状况及行程信息**未改变且长期稳定**时的自动填报！当健康状况发生改变时请**立即**停止使用脚本并**手动填报**信息，积极配合疫情防控措施！因滥用脚本造成的法律后果请自行承担！！</font>

## 功能

可实现健康状况正常时的自动填报。支持为多个用户填报，并将填报结果分别推送至每个用户的 iOS 设备。

## 实现

通过向网站发送正常填报时发送的数据包模拟正常填报过程。一些必要的参数是从响应的 HTML 文本中分析文本特点截取的。详细过程可参考 `login.py` 模块。

填报结果通过 iOS 端的 Bark 应用推送至设备。

2022.04.17 更新：平台本周为填报表格增加了隐藏参数并为每个按钮分配了不同的请求 ID，使得原有脚本失效，已针对此变化更新了填报流程。

## 使用

因脚本仅自用，故未预留前端接口，未采用参数形式传入用户配置文件，需手动配置后台。未对用户配置文件作有效性检查，无效的用户配置文件会导致不可预料的错误。

`zzujksb.py` 为主程序文件，`reset_pending.sh` 用于自动重置待上报的用户，注意需为其添加执行权限。原始用户数据存储于 `users-available/`，可存放多个用户，将需要激活的用户数据文件建立软链接于 `users-enabled/` 中即可。
```
$ ln -s ../users-available/users-to-activate.json ./users-enabled/
```
`users-available/example.json` 为用户信息样例，各名称代表含义如下：

`city` 代表当前所在城市的行政区划代码。脚本中未内置各城市的行政区划代码，可通过搜索引擎检索得到。示例文件中的 `4101` 表示郑州。`address` 表示当前所在详细地址。

`longitude`，`laptitude` 分别表示经度、纬度，样例中为郑州大学钟楼的坐标。请填写真实坐标，随意填写坐标会导致后台判定用户离市或离省，影响请假与销假。

`vaccine` 表示疫苗接种情况，从 `1` 到 `5` 分别代表已接种第一针剂、已接种第二针剂、尚未接种、因禁忌症无法接种、已接种第三针剂。

`cookie` 为自动登录所使用的 cookie，脚本中有自动获取 cookie 的代码，留空即可。

`barkid` 为 iOS 平台利用 Bark 统一推送的设备 ID，可在 iOS 设备上安装 Bark 应用后获取 ID 填入，实现将打卡结果推送到 iOS 设备的功能，避免因程序运行错误而错过打卡。

注：根据 json 语法，请保留各键值对的双引号。

可利用 cron 定时任务实现自动化。
```
$ crontab -e
```
添加任务示例：
```
0 0 * * * /path/to/zzujksb/reset_pending.sh  # 每日 0 时自动重置待上报用户
30 1-8 * * * python3 /path/to/zzujksb/zzujksb.py  # 凌晨 1-8 时每小时的第 30 分钟执行一次自动上报
```
无论成功与否，`zzujksb.py` 仅会为每个用户执行一次自动填报，不会重复提交，上报结果将推送至配置文件中 `barkid` 项所指定的 iOS 设备。

根据经验，凌晨 12:00-12:15 为高峰期，填报失败概率较大，建议避开此时段。

## 兼容性

测试平台：Ubuntu 20.04

Python 版本：3.x

## 依赖

发送 HTTP 请求需要安装 `requests` 模块，可执行 `pip list` 检查是否安装。

安装 `requests` 模块：
```
$ sudo pip install requests
```
在 Raspbian OS 上测试时，内置的 Python 3.7.3 中缺失 `urllib` 模块，自行编译安装新版本后问题解决。

## 关于

此脚本已引入 GPL 协议，请遵守协议要求。

开源此脚本仅为技术交流，欢迎讨论相关话题。

切勿以违反法律的方式使用代码。虽然 GPL 协议本身未禁止商用行为，但是利用本程序协助他人填报健康状况牟利仍存在法律风险，作者不承担因滥用导致的法律责任。

## 一些废话

有能力找到这里并且会配置这样的脚本的人，应该都不会满足于用别人现成的代码了吧……其实实现过程并不难，网站也并不复杂，利用 Burp Suite 抓包就可以轻松看出填报流程了。奈何本人非计算机科班出身，水平实在有限，写的时候 Bug 频出，本来很简单的流程写了很久才完成 T_T。代码的实现也比较暴力，从响应的 HTML 文本中截取参数的方法暴力至极(T_T)。已经有很多大佬做出了很棒的实现，重复造了一遍轮子权当练手。建议感兴趣又不清楚实现细节的同学自己实现一遍^_^

之所以选用 Bark 推送结果而不是邮箱，因为作者本人使用的是 iOS 设备，直接使用统一推送平台的体验比邮箱好很多，配置还简单，而且邮箱的实现也有很多大佬做过了，就不重复实现了（低情商：偷个懒）。