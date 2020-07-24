'''
author:曹世皎、张敬民、费一朔
create time:2020-07-15
update time:2020-07-17
'''

import requests
import base64
import pandas as pd
import json
from builtins import str

#车辆损伤识别
def damageIdentification(path):
    #车辆损伤识别access_token获取
    host = 'https://aip.baidubce.com/oauth/2.0/token?'
    params = {
        "grant_type": "client_credentials",
        "client_id": "GIsibzvkARvBEQE8kprpVq63",
        "client_secret": "Axm9V8zjodY1hdPrQqmPne5j747pHP2b"
    }
    response = requests.get(host, params=params)
    # display(pd.json_normalize(response.json()).T)
    # print(pd.json_normalize(response.json()).T)

    access_token = response.json()["access_token"]
    access_token

    '''
    车辆外观损伤识别
    '''
    #车辆损伤识别url
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/vehicle_damage"
    # 二进制方式打开图片文件
    f = open(path, 'rb')
    img = base64.b64encode(f.read())

    params = {"image": img}
    # access_token = '[调用鉴权接口获取的token]'
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)

    # if response:
    # print (response.json())

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
    e = d['result']
    # print(e)
    # print(e['damage_info'])
    # print(c.count('parts'))

    #返回识别结果
    total_num = c.count('parts')
    str5 = {}
    for i in range(0, total_num):
        str1 = "受损部位：" + str(e['damage_info'][i]['parts']) + '\n'
        str2 = "受损情况：" + str(e['damage_info'][i]['type']) + '\n'
        str3 = "概率：" + "0." + str(e['damage_info'][i]['probability']) + '\n'
        # print("受损部位：",e['damage_info'][i]['parts'])
        # print("受损情况：",e['damage_info'][i]['type'])
        # print("0.",e['damage_info'][i]['probability'])
        str4 = str1 + str2 + str3
        str5[i] = str4
    return str5
# str6=chesun('static/picture/11.png')
# print(str6)


# damage_info=get_str_btw(c,"parts\": ",", ")
# print(damage_info)
# print (get_str_btw(c,"parts\": ",", "))
