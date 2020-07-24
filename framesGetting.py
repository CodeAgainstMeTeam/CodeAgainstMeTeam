'''
author:朱一凡
create time:2020-07-21
update time:2020-07-21
'''

import cv2
import numpy as np

#对视频进行分帧处理
def getFrames():
    video = cv2.VideoCapture('static/picture/video1.mp4')
    ok, frame = video.read()
    count = 0
    while ok:
        cv2.imwrite("data/frame%d.jpg"%(count), frame)
        print('WRITTEN FRAME:',count)
        count+=1
        ok, frame = video.read()
    video.release()

getFrames()