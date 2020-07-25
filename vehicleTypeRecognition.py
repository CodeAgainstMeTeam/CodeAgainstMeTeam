'''
author:曹世皎、尹迎春
create time:2020-07-13
update time:2020-07-17
'''

import os
import argparse
import numpy as np
import cv2

#车型检测
def vehicleTypeRecognition(image):
    weightsPath = "yolov3.weights"
    configPath = "yolov3.cfg"
    labelsPath = "coco.names"
    # rootdir = "data/street"  # 图像读取地址
    # savepath = "data/divided_img"  # 图像保存地址
    model = cv2.dnn.readNetFromCaffe("model/vehicle_model.prototxt", "model/vehicle_model.caffemodel")
    mean_rgb = [123.68, 116.779, 103.939]
    std_rgb = [58.393, 57.12, 57.375]

    # ---------------------------------------------------------------------------------------------------------
    # 初始化一些参数
    LABELS = open(labelsPath).read().strip().split("\n")  # 物体类别
    COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")  # 颜色

    # filelist = os.listdir(rootdir)  # 打开对应的文件夹
    # total_num = len(filelist)  # 得到文件夹中图像的个数
    # print(total_num)
    # 如果输出的文件夹不存在，创建即可
    # if not os.path.isdir(savepath):
    #   os.makedirs(savepath)

    # for (dirpath, dirnames, filenames) in os.walk(rootdir):
    # for filename in filenames:
    # 必须将boxes在遍历新的图片后初始化d

    boxes = []
    confidences = []
    classIDs = []
    net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
    #  path = os.path.join(dirpath, filename)
    # image = cv2.imread(path)
    (H, W) = image.shape[:2]
    # 得到 YOLO需要的输出层
    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    # 从输入图像构造一个blob，然后通过加载的模型，给我们提供边界框和相关概率
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    layerOutputs = net.forward(ln)
    # 在每层输出上循环
    for output in layerOutputs:
        # 对每个检测进行循环
        for detection in output:
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]
            # 过滤掉那些置信度较小的检测结果
            if confidence > 0.5:
                # 框后接框的宽度和高度
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")
                # 边框的左上角
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))
                # 更新检测出来的框
                # 批量检测图片注意此处的boxes在每一次遍历的时候要初始化，否则检测出来的图像框会叠加
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)
    # 极大值抑制
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.3, 0.3)
    k = -1
    if len(idxs) > 0:
        # for k in range(0,len(boxes)):
        for i in idxs.flatten():
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])

            # 图像裁剪注意坐标要一一对应
            # 图片裁剪 裁剪区域【Ly:Ry,Lx:Rx】
            cut = image[y:(y + h), x:(x + w)]
            # ==========================================================================
            aligned = cv2.resize(cut, (224, 224), interpolation=cv2.INTER_CUBIC)
            im_tensor = np.zeros((1, 3, 224, 224))
            for i in range(3):
                im_tensor[0, i, :, :] = (aligned[:, :, 2 - i] / 1.0 - mean_rgb[2 - i]) / std_rgb[2 - i]
            model.setInput(im_tensor)
            _embedding = model.forward()[0]

            # print( _embedding.transpose().max() )
            idx = _embedding.transpose().argmax()
            label = open("label.txt", "r", encoding="UTF8")
            label_txt = label.readlines()
            # print( label_txt[idx] )
            text1 = label_txt[idx]
            text2 = _embedding.transpose().max()
            text = str(idx)

            # ==================================================================================
            # 在原图上绘制边框和类别
            color = (0, 0, 255)
            # image是原图，左上点坐标， 右下点坐标， 颜色， 画线的宽度
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
            # text = "{}: {:.4f}".format( LABELS[classIDs[i]], confidences[i] )
            # 各参数依次是：图片，添加的文字，左上角坐标(整数)，字体字体大小，颜色，字体粗细
            cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            # boxes的长度即为识别出来的车辆个数，利用boxes的长度来定义裁剪后车辆的路径名称
            if k < len(boxes):
                k = k + 1
            # 从字母a开始每次+1
            t = chr(ord("a") + k)
            # 写入文件夹，不支持int，故用字母
            # cv2.imwrite(savepath + "/" + filename.split(".")[0] + "_" + t + ".jpg", cut)
            # # 调用cv.2的imwrite函数保存图片
            # save_path = dirpath + "/"
            # if os.path.exists(save_path):
            #     # print(i)
            #     save_img= save_path+ '_new' + filename
            #     cv2.imwrite(save_img, image)
            # else:
            #     os.mkdir(save_path)
            #     save_img = save_path + '_new'+ filename
            #     cv2.imwrite(save_img, image)
            return image, idx, text1, text2

# 训练代码
# img=cv2.imread('static/picture/05.jpg')
# img,t,t1 ,t2=cxsb(img)
# print(t)
# print(t2)
# print(t1)
# def softmax(x):
#     """Compute softmax values for each sets of scores in x."""
#     pass  # TODO: Compute and return softmax(x)
#     x = np.array(x)
#     x = np.exp(x)
#     x.astype('float32')
#     if x.ndim == 1:
#         sumcol = sum(x)
#         for i in range(x.size):
#             x[i] = x[i]/float(sumcol)
#     if x.ndim > 1:
#         sumcol = x.sum(axis = 0)
#         for row in x:
#             for i in range(row.size):
#                 row[i] = row[i]/float(sumcol[i])
#     return x
#
# def softmax_2(x):
#     return np.exp(x)/np.sum(np.exp(x),axis=0)

# 车型识别代码
# aligned = cv2.resize(cut, (224, 224), interpolation=cv2.INTER_CUBIC)
# im_tensor = np.zeros((1, 3, 224, 224))
# for i in range(3):
#     im_tensor[0, i, :, :] = (aligned[:, :, 2 - i] / 1.0 - mean_rgb[2 - i]) / std_rgb[2 - i]
#
# model.setInput(im_tensor)
# _embedding = model.forward()[0]
#
# print(_embedding.transpose().max())
# idx = _embedding.transpose().argmax()
# label = open("label.txt", "r", encoding="UTF-8")
# label_txt = label.readlines()
# print(label_txt[idx])
