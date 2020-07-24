'''
author:张敬民、费一朔
create time:2020-07-14
update time:2020-07-18
'''

from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

import sys
import HyperLPRLite as pr
import cv2
import numpy as np
import time
import importlib

# sys.setdefaultencoding("utf-8")


fontC = ImageFont.truetype("./Font/platech.ttf", 14, 0)

#对车牌进行定位处理
def drawRectBox(image, rect, addText):
    cv2.rectangle(image, (int(rect[0]), int(rect[1])), (int(rect[0] + rect[2]), int(rect[1] + rect[3])), (0, 0, 255), 2,
                  cv2.LINE_AA)
    cv2.rectangle(image, (int(rect[0] - 1), int(rect[1]) - 16), (int(rect[0] + 115), int(rect[1])), (0, 0, 255), -1,
                  cv2.LINE_AA)
    img = Image.fromarray(image)
    draw = ImageDraw.Draw(img)
    draw.text((int(rect[0] + 1), int(rect[1] - 16)), addText, (255, 255, 255), font=fontC)
    imagex = np.array(img)
    return imagex

#在原识别图像中标注识别结果
def visual_draw_position(image_path):
    max = 0
    maxcp = ''
    grr = cv2.imread(image_path)
    model = pr.LPR("model/cascade.xml", "model/model12.h5", "model/ocr_plate_all_gru.h5")
    for pstr, confidence, rect in model.SimpleRecognizePlateByE2E(grr):
        if confidence > max:
            max = confidence
            maxcp = pstr
        grr = drawRectBox(grr, rect, pstr + " " + str(round(confidence, 3)))
    return grr, maxcp, max

# SpeedTest("images_rec/2.jpg")
