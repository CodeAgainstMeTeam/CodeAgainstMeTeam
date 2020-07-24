'''
author:朱一凡、张敬民
create time:2020-07-15
update time:2020-07-17
'''

# encoding:utf-8

import requests
import base64
import re
import json
import cv2

'''
车辆检测
'''

#车辆检测
def vehicleDetection1(path):
    #车辆检测url
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/vehicle_detect"
    # 二进制方式打开图片文件
    f = open(path, 'rb')
    img = base64.b64encode(f.read())
    image = cv2.imread(path)

    #车辆检测access_token获取
    params = {"image": img}
    access_token = '24.bb863d090ea1d366750f030ff7018074.2592000.1597628778.282335-21452043'
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)

    # 处理返回的json数据
    a = response.json()
    b = json.dumps(a)
    c = str(b)
    d = json.loads(b)
    e = d['vehicle_info']
    # 获取两个指定字符串中间的内容
    def get_str_btw(s, f, b):
        par = s.partition(f)
        return (par[2].partition(b))[0][:]

    motorbike_num = int(get_str_btw(c, "bike\": ", ", "))
    tricycle_num = int(get_str_btw(c, "cycle\": ", ", "))
    car_num = int(get_str_btw(c, "car\": ", ", "))
    truck_num = int(get_str_btw(c, "truck\": ", ", "))
    bus_num = int(get_str_btw(c, "bus\": ", "}"))

    total_num = motorbike_num + tricycle_num + car_num + truck_num + bus_num
    print("total_num: ", total_num)

    # if response:
    #     print (response.json())

    #标记检测出来的车辆
    for i in range(0, total_num):
        cv2.rectangle(image, (e[i]['location']['left'], e[i]['location']['top']), (
        e[i]['location']['left'] + e[i]['location']['width'], e[i]['location']['top'] + e[i]['location']['height']),
                      (0, 255, 0), 2)
        if (e[i]['location']['top'] > 10):
            cv2.putText(image, e[i]['type'], (e[i]['location']['left'], e[i]['location']['top'] - 6),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (0, 255, 0))
        else:
            cv2.putText(image, e[i]['type'], (e[i]['location']['left'], e[i]['location']['top'] + 15),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (0, 255, 0))

    #返回标记过后的图片并返回统计数据
    cv2.imwrite(
        'C:\\Users\\1\\Desktop\\Vehicle-Car-detection-and-multilabel-classification-master\\test_result\\test_6.jpg',
        image)
    return image, motorbike_num, tricycle_num, car_num, truck_num, bus_num
# image,motorbike_num,tricycle_num,car_num,truck_num,bus_num=vehicleDetection1('static/picture/50.jpg')
