'''
author:曹世皎、张敬民
create time:2020-07-21
update time:2020-07-23
'''



# encoding:utf-8
import requests
import base64
import pandas as pd
import json
import os

#车辆外观属性识别
def attributeIdentification(path):
    #车辆属性识别access_token获取
    host = 'https://aip.baidubce.com/oauth/2.0/token?'
    params = {
        "grant_type":"client_credentials",
        "client_id":"9bV5xsYshttfW64I4nvsAj7P",
        "client_secret":"2ugDsIE9tqEHC2yQiPPmMLwqPM7ombTH"
    }
    response = requests.get(host,params=params)
    # display(pd.json_normalize(response.json()).T)
    # print(pd.json_normalize(response.json()).T)
    access_token=response.json()["access_token"]
    access_token


    '''
    车辆属性识别
    '''

    #车辆属性识别url
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/vehicle_attr"
    # 二进制方式打开图片文件
    f = open(path, 'rb')
    img = base64.b64encode(f.read())

    params = {"image":img}
    # access_token = '[调用鉴权接口获取的token]'
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        print (response.json())

    #获取两个指定字符串中间的内容
    def get_str_btw(s, f, b):
        par = s.partition(f)
        return (par[2].partition(b))[0][:]

    #处理返回的json数据
    a=response.json()
    b=json.dumps(a)
    c=str(b)
    d=json.loads(b)
    # print(d)
    e=d['vehicle_info']
    print(e)

    total_num=c.count('attributes')
    print (total_num)

    #返回识别结果
    str17 = []
    str18 =[]
    for i in range(0, total_num):
        str1 = "车辆类型：" + str(e[i]['attributes']['vehicle_type']['name']) +str(format(e[i]['attributes']['vehicle_type']['score'], '.3f'))
        if e[i]['attributes']['direction'] is not None:
            str2 = "车辆朝向：" + str(e[i]['attributes']['direction']['name'])+str(format(e[i]['attributes']['direction']['score'],'.3f'))
        str3 = "驾驶位系安全带：" + str(format(e[i]['attributes']['driver_belt']['score'], '.3f'))
        str4 = "副驾驶位系安全带：" + str(format(e[i]['attributes']['copilot_belt']['score'], '.3f'))
        str5 = "驾驶位遮阳板放下：" + str(format(e[i]['attributes']['driver_visor']['score'], '.3f'))
        str6 = "副驾驶位遮阳板放下：" + str(format(e[i]['attributes']['copilot_visor']['score'], '.3f'))
        str7 = "副驾驶有人：" + str(format(e[i]['attributes']['copilot']['score'], '.3f'))
        str8 = "有后视镜悬挂物：" + str(format(e[i]['attributes']['rearview_item']['score'], '.3f'))
        str9 = "有车内摆放物：" + str(format(e[i]['attributes']['in_car_item']['score'], '.3f'))
        str10 = "有天窗：" + str(format(e[i]['attributes']['skylight']['score'], '.3f'))
        str11 = "有车窗雨眉：" + str(format(e[i]['attributes']['window_rain_eyebrow']['score'], '.3f'))
        str12 = "检测框宽度：" + str(e[i]['location']['width'])
        str13 = "检测框顶坐标：" + str(e[i]['location']['top'])
        str14 = "检测框左坐标：" + str(e[i]['location']['left'])
        str15 = "检测框高度：" + str(e[i]['location']['height'])
        # str16 = str1 + str2 + str3+ str4 + str5 + str6 + str7 + str8 + str9 + str10 + str11 + str12 + str13 + str14 + str15
        str17.append(str1)
        str17.append(str2)
        str17.append(str3)
        str17.append(str4)
        str17.append(str5)
        str17.append(str6)
        str17.append(str7)
        str17.append(str8)
        str17.append(str9)
        str17.append(str10)
        str17.append(str11)
        str17.append(str12)
        str17.append(str13)
        str17.append(str14)
        str17.append(str15)

        str18.append(str17)




    return str18


    # for i in range(0,total_num):
    #     print("车辆朝向：",e[i]['attributes']['direction']['name'],format(e[i]['attributes']['direction']['score'], '.3f') )
    #     print("副驾驶位是否系安全带：",format(e[i]['attributes']['copilot_belt']['score'], '.3f'))
    #     print("副驾驶位遮阳板是否放下：",format(e[i]['attributes']['copilot_visor']['score'], '.3f'))
    #     print("是否有后视镜悬挂物：", format(e[i]['attributes']['rearview_item']['score'], '.3f'))
    #     print("驾驶位遮阳板是否放下：", format(e[i]['attributes']['driver_visor']['score'], '.3f'))
    #     print("是否有车内摆放物：", format(e[i]['attributes']['in_car_item']['score'], '.3f'))
    #     print("是否有天窗：", format(e[i]['attributes']['skylight']['score'], '.3f'))
    #     print("副驾驶是否有人：", format(e[i]['attributes']['copilot']['score'], '.3f'))
    #     print("是否有车窗雨眉：",format(e[i]['attributes']['window_rain_eyebrow']['score'], '.3f'))
    #     print("车辆类型：",e[i]['attributes']['vehicle_type']['name'],format(e[i]['attributes']['vehicle_type']['score'], '.3f'))
    #     print("驾驶位是否系安全带：",format(e[i]['attributes']['driver_belt']['score'], '.3f'))
    #     print("检测框宽度：",e[i]['location']['width'])
    #     print("检测框顶坐标：",e[i]['location']['top'])
    #     print("检测框左坐标：",e[i]['location']['left'])
    #     print("检测框高度：",e[i]['location']['height'])





