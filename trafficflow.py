'''
author:曹世皎、朱一凡
create time:2020-07-22
update time:2020-07-24
'''

#额外功能、暂时舍弃

# encoding:utf-8
import requests
import base64
import cv2
import numpy as np

'''
车流统计
'''

#对图像进行分帧处理
def getFrames():
    video = cv2.VideoCapture('static/picture/video1.mp4')
    ok, frame = video.read()
    count = 0
    while ok:
        cv2.imwrite("C:/Users/Lenovo/Desktop/untitled6/untitled6/data/frame%d.jpg"%(count), frame)
        # print('WRITTEN FRAME:',count)
        count+=1
        ok, frame = video.read()
    video.release()
    return count

n = getFrames()

request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/traffic_flow"
# 二进制方式打开图片文件
# for i in (0,n-1):
#     f = open('C:/Users/Lenovo/Desktop/untitled6/untitled6/data/frame%d.jpg' %(i), 'rb')
f = open('C:/Users/Lenovo/Desktop/untitled6/untitled6/data/frame0.jpg', 'rb')
img = base64.b64encode(f.read())

#定义识别框大小，是否返回处理结果图等
params = {"area":"1,1,719,1,719,719,1,719","case_id":1,"case_init":"false","image":img}
access_token = '24.7cb3fe592d321ebb2ba3a98f125e5469.2592000.1597992978.282335-21517406'
request_url = request_url + "?access_token=" + access_token
headers = {'content-type': 'application/x-www-form-urlencoded'}
response = requests.post(request_url, data=params, headers=headers)
if response:
    print (response.json())