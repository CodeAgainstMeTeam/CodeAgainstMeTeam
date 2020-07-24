'''
author:曹世皎、张敬民、费一朔
create time:2020-07-17
update time:2020-07-19
'''

# encoding:utf-8
import requests
import base64
import pandas as pd
import json

#驾驶行为分析
def drivingBehaviorAnalysis(path):
    #驾驶行为分析access_token获取
    host = 'https://aip.baidubce.com/oauth/2.0/token?'
    params = {
        "grant_type": "client_credentials",
        "client_id": "wVA90rK7TdcTEIe9zUGlxHKG",
        "client_secret": "NKo4rbOlQmEpG1mGfB3ONEudiyq0Nov2"
    }
    response = requests.get(host, params=params)
    # display(pd.json_normalize(response.json()).T)
    # print(pd.json_normalize(response.json()).T)

    access_token = response.json()["access_token"]
    access_token

    '''
    驾驶行为分析
    '''
    #驾驶行为分析url
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/driver_behavior"
    # 二进制方式打开图片文件
    f = open(path, 'rb')
    img = base64.b64encode(f.read())

    params = {"image": img}
    # access_token = '[调用鉴权接口获取的token]'
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        print(response.json())

    # 获取两个指定字符串中间的内容
    def get_str_btw(s, f, b):
        par = s.partition(f)
        return (par[2].partition(b))[0][:]

    # 处理返回的json数据
    a = response.json()
    b = json.dumps(a)
    c = str(b)
    d = json.loads(b)
    # print(d)
    e = d['person_info']
    print(e)
    # print(e['damage_info'])
    # print(c.count('parts'))
    total_num = c.count('location')
    print(total_num)

    #返回分析结果
    for i in range(0, total_num):
        both_hands_leaving_wheel = "双手离开方向盘：" + str(
            format(e[i]['attributes']['both_hands_leaving_wheel']['score'], '.3f'))
        eyes_closed = "闭眼：" + str(format(e[i]['attributes']['eyes_closed']['score'], '.3f'))
        no_face_mask = "未正确佩戴口罩：" + str(format(e[i]['attributes']['no_face_mask']['score'], '.3f'))
        not_buckling_up = "未系安全带：" + str(format(e[i]['attributes']['not_buckling_up']['score'], '.3f'))
        smoke = "吸烟：" + str(format(e[i]['attributes']['smoke']['score'], '.3f'))
        cellphone = "使用手机：" + str(format(e[i]['attributes']['cellphone']['score'], '.3f'))
        not_facing_front = "视角未朝前方：" + str(format(e[i]['attributes']['not_facing_front']['score'], '.3f'))
        yawning = "打哈欠：" + str(format(e[i]['attributes']['yawning']['score'], '.3f'))
        head_lowered = "低头：" + str(format(e[i]['attributes']['head_lowered']['score'], '.3f'))
        # print("双手离开方向盘：",format(e[i]['attributes']['both_hands_leaving_wheel']['score'], '.3f') )
        # print("闭眼：",format(e[i]['attributes']['eyes_closed']['score'], '.3f'))
        # print("未正确佩戴口罩：",format(e[i]['attributes']['no_face_mask']['score'], '.3f'))
        # print("未系安全带：", format(e[i]['attributes']['not_buckling_up']['score'], '.3f'))
        # print("吸烟：", format(e[i]['attributes']['smoke']['score'], '.3f'))
        # print("视角未朝前方：", format(e[i]['attributes']['cellphone']['score'], '.3f'))
        # print("使用手机：", format(e[i]['attributes']['not_facing_front']['score'], '.3f'))
        # print("打哈欠：", format(e[i]['attributes']['yawning']['score'], '.3f'))
        # print("低头：",format(e[i]['attributes']['head_lowered']['score'], '.3f'))
        return both_hands_leaving_wheel, eyes_closed, no_face_mask, not_buckling_up, smoke, cellphone, not_facing_front, yawning, head_lowered
