# coding=utf-8
import requests
import json

# 设置Server酱post地址 不需要可以删除
serverChan = "https://sc.ftqq.com/*****************************************.send"
# 状态地址
current_url = 'https://zhiyou.smzdm.com/user/info/jsonp_get_current'
# 签到地址
checkin_url = 'https://zhiyou.smzdm.com/user/checkin/jsonp_checkin'
# 用用户名和密码登录后获取Cookie
userCookie = "**************************************************************"
headers = {
    'Referer': 'https://www.smzdm.com/',
    'Host': 'zhiyou.smzdm.com',
    'Cookie': 'sess=AT-yZQzXKzdSC7o3YnwX0OpkjocvLg5u+l5t8G0BIrX20iFF64RR1lyh9jhciU5/3KO84rt4Oq1au+Of/CDR2LuQySal/zshF8Vro7c4vDYJM6Wr/ApUYLvoq2C; user=user:5067542215|5067542215; smzdm_id=xxx5067542215;',
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
}


def req(url):
    url = url
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        data = json.loads(res.text)
        return data
    else:
        print(res.status_code)
        print(res.text)


data = req(current_url)
if data['checkin']['has_checkin']:
    info = '[ZDM]%s---> %s, 已经签到：%s天' % (data['sys_date'], data['nickname'], data['checkin']['daily_checkin_num'])
    print(info)
else:
    checkin = req(checkin_url)['data']
    # print(checkin)
    info = time.strftime('[ZDM]%Y.%m.%d %H:%M:%S', time.localtime(time.time())) + '---> 签到成功，签到天数%s' % (checkin['checkin_num'])
    print(info)

print()

# sshpass -p '@@9HLx63RwWMAe' scp -r ./zdm.py root@106.75.148.48:/root
# sshpass -p '9HLx63RwWMAe' scp -P 26807 -r zdm.py root@144.168.63.235:/root