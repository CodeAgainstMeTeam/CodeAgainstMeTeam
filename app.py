'''
author:张敬民、费一朔、尹迎春
create time:2020-07-13
update time:2020-07-24
'''

import base64
from io import BytesIO
from PIL import Image
from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify, Response
from werkzeug.utils import secure_filename
from camera import VideoCamera
import damageIdentification
import licenseRecognition
import vehicleDetection
import vehicleTypeRecognition
import attributeIdentification
import drivingBehaviorAnalysis
from datetime import timedelta
import os
import requests
import cv2
from tensorflow.python.keras import Sequential
import time

classifier = Sequential()

# 设置允许的文件格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])


# 通过url下载图片，并保存至static/picture
def download_img(img_url):
    basepath = os.path.dirname(__file__)

    path = basepath + '/' + 'static/picture' + '/' "test" + '.jpg'
    response = requests.get(img_url)
    image = Image.open(BytesIO(response.content))
    ls_f = base64.b64encode(BytesIO(response.content).read()).decode('utf-8')
    imgdata = base64.b64decode(ls_f)
    file = open(path, 'wb')
    file.write(imgdata)
    file.close()
    return"test" + '.jpg'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


app = Flask(__name__)
# 设置静态文件缓存过期时间
app.send_file_max_age_default = timedelta(seconds=1)

#车型识别模块
@app.route("/cxsb", methods=['POST'])  # 添加路由
def cxsb():
    if request.method == 'POST':

        url = request.form.get('url')
        f = request.files['file']
        if url =='':

            if not (f and allowed_file(f.filename)):
                return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})

            user_input = request.form.get("name")

            basepath = os.path.dirname(__file__)  # 当前文件所在路径

            upload_path = os.path.join(basepath, 'static/picture',
                                       secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径

            f.save(upload_path)

            print('static/picture/' + f.filename)
            image = cv2.imread('static/picture/' + f.filename)

            image_rectangle, id, cx, confidence = vehicleTypeRecognition.vehicleTypeRecognition(image)  # 车型检测

            name = f.filename.split(".")[0] + "_rectangle" + ".jpg"
            upload_path1 = os.path.join(basepath, 'static/picture', secure_filename(name))
            # image = Image.fromarray(cv2.cvtColor(imagekuang, cv2.COLOR_BGR2RGB))
            # image_rectangle.save(upload_path1)
            cv2.imwrite(upload_path1, image_rectangle)
            # 使用Opencv转换一下图片格式和名称
            return render_template('index.html', cx="picture/" + name, cxid=id, cxh=cx, val1=time.time())
        else:
            base=url[0:21]
            if base.find("base64"):
                url64=url[22:]
                basepath = os.path.dirname(__file__)
                imgdata = base64.b64decode(url64)
                name="test"+ '.png'
                file = open('static/picture/'+ '/' + "test" + '.png', 'wb')
                file.write(imgdata)
                file.close()
                image = cv2.imread('static/picture/' + name)
                print(name)
                image_rectangle, id, cx, confidence = vehicleTypeRecognition.vehicleTypeRecognition(image)  # 车型检测

                name = "test1.jpg".split(".")[0] + "_rectangle" + ".jpg"
                upload_path1 = os.path.join(basepath, 'static/picture', secure_filename(name))
                # image = Image.fromarray(cv2.cvtColor(imagekuang, cv2.COLOR_BGR2RGB))
                # image_rectangle.save(upload_path1)
                cv2.imwrite(upload_path1, image_rectangle)
                # 使用Opencv转换一下图片格式和名称
                return render_template('index.html', cx="picture/" + name, cxid=id, cxh=cx, val1=time.time())
            else:
                filename=download_img(url)
                basepath = os.path.dirname(__file__)
                image = cv2.imread('static/picture/' + filename)
                print(filename)
                image_rectangle, id, cx, confidence = vehicleTypeRecognition.vehicleTypeRecognition(image)  # 车型检测

                name = filename.split(".")[0] + "_rectangle" + ".jpg"
                upload_path1 = os.path.join(basepath, 'static/picture', secure_filename(name))
                # image = Image.fromarray(cv2.cvtColor(imagekuang, cv2.COLOR_BGR2RGB))
                # image_rectangle.save(upload_path1)
                cv2.imwrite(upload_path1, image_rectangle)
                # 使用Opencv转换一下图片格式和名称
                return render_template('index.html', cx="picture/" + name, cxid=id, cxh=cx, val1=time.time())

#车牌识别模块
@app.route("/cpsb", methods=['POST'])  # 添加路由
def cpsb():
    if request.method == 'POST':
        url = request.form.get('url')
        f = request.files['file']
        if url == '':
            if not (f and allowed_file(f.filename)):
                return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})

            user_input = request.form.get("name")

            basepath = os.path.dirname(__file__)  # 当前文件所在路径

            upload_path = os.path.join(basepath, 'static/picture',
                                       secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
            f.save(upload_path)
            path = 'static/picture/' + f.filename
            print('static/picture/' + f.filename)
            image = cv2.imread('static/picture/' + f.filename)
            img, res, confidence = licenseRecognition.visual_draw_position(path)

            name = f.filename.split(".")[0] + "_rec" + ".jpg"
            upload_path1 = os.path.join(basepath, 'static/picture', secure_filename(name))

            cv2.imwrite(upload_path1, img)

            return render_template('index.html', cp="picture/" + name, cpsbresult=res, confidence2=confidence,
                                   val1=time.time())
        else:
            base = url[0:21]
            if base.find("base64"):
                url64 = url[22:]
                basepath = os.path.dirname(__file__)
                imgdata = base64.b64decode(url64)
                name = "test" + '.png'
                path = 'static/picture/' + name
                file = open('static/picture/' + '/' + "test" + '.png', 'wb')
                file.write(imgdata)
                file.close()
                image = cv2.imread('static/picture/' + name)
                print(name)
                img, res, confidence = licenseRecognition.visual_draw_position(path)

                name = f.filename.split(".")[0] + "_rec" + ".jpg"
                upload_path1 = os.path.join(basepath, 'static/picture', secure_filename(name))

                cv2.imwrite(upload_path1, img)

                return render_template('index.html', cp="picture/" + name, cpsbresult=res, confidence2=confidence,
                                       val1=time.time())
            else:
                filename = download_img(url)
                path = 'static/picture/' + filename
                basepath = os.path.dirname(__file__)
                image = cv2.imread('static/picture/' + filename)
                img, res, confidence = licenseRecognition.visual_draw_position(path)

                name = filename.split(".")[0] + "_rec" + ".jpg"
                upload_path1 = os.path.join(basepath, 'static/picture', secure_filename(name))

                cv2.imwrite(upload_path1, img)

                return render_template('index.html', cp="picture/" + name, cpsbresult=res, confidence2=confidence,
                                       val1=time.time())

#车辆检测模块
@app.route("/cljc", methods=['POST'])  # 添加路由
def cljc():
    if request.method == 'POST':

        url = request.form.get('url')
        f = request.files['file']
        if url == '':
            if not (f and allowed_file(f.filename)):
                return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})
            user_input = request.form.get("name")
            basepath = os.path.dirname(__file__)  # 当前文件所在路径
            upload_path = os.path.join(basepath, 'static/picture',
                                       secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
            f.save(upload_path)
            path = 'static/picture/' + f.filename
            print(path)
            image = cv2.imread('static/picture/' + f.filename)
            image_rec, motorbike_num, tricycle_num, car_num, truck_num, bus_num = vehicleDetection.vehicleDetection1(path)
            name = f.filename.split(".")[0] + "_rectangle1" + ".jpg"
            upload_path1 = os.path.join(basepath, 'static/picture', secure_filename(name))
            # image = Image.fromarray(cv2.cvtColor(imagekuang, cv2.COLOR_BGR2RGB))
            # image_rectangle.save(upload_path1)
            cv2.imwrite(upload_path1, image_rec)

            return render_template('index.html', cljc="picture/" + name, motorbike_num=motorbike_num,
                                   tricycle_num=tricycle_num, car_num=car_num, truck_num=truck_num, bus_num=bus_num,
                                   val1=time.time())
        else:
            base = url[0:21]
            if base.find("base64"):
                url64 = url[22:]
                basepath = os.path.dirname(__file__)
                imgdata = base64.b64decode(url64)
                name = "test" + '.png'
                path = 'static/picture/' + name
                file = open('static/picture/' + '/' + "test" + '.png', 'wb')
                file.write(imgdata)
                file.close()
                image = cv2.imread('static/picture/' + name)
                print(name)
                image_rec, motorbike_num, tricycle_num, car_num, truck_num, bus_num = vehicleDetection.vehicleDetection1(
                    path)
                name = f.filename.split(".")[0] + "_rectangle1" + ".jpg"
                upload_path1 = os.path.join(basepath, 'static/picture', secure_filename(name))
                # image = Image.fromarray(cv2.cvtColor(imagekuang, cv2.COLOR_BGR2RGB))
                # image_rectangle.save(upload_path1)
                cv2.imwrite(upload_path1, image_rec)

                return render_template('index.html', cljc="picture/" + name, motorbike_num=motorbike_num,
                                       tricycle_num=tricycle_num, car_num=car_num, truck_num=truck_num, bus_num=bus_num,
                                       val1=time.time())
            else:
                filename = download_img(url)
                path = 'static/picture/' + filename
                basepath = os.path.dirname(__file__)
                image = cv2.imread('static/picture/' + filename)
                image_rec, motorbike_num, tricycle_num, car_num, truck_num, bus_num = vehicleDetection.vehicleDetection1(
                    path)
                name = filename.split(".")[0] + "_rectangle1" + ".jpg"
                upload_path1 = os.path.join(basepath, 'static/picture', secure_filename(name))
                # image = Image.fromarray(cv2.cvtColor(imagekuang, cv2.COLOR_BGR2RGB))
                # image_rectangle.save(upload_path1)
                cv2.imwrite(upload_path1, image_rec)

                return render_template('index.html', cljc="picture/" + name, motorbike_num=motorbike_num,
                                       tricycle_num=tricycle_num, car_num=car_num, truck_num=truck_num, bus_num=bus_num,
                                       val1=time.time())

#车损识别模块
@app.route("/cssb", methods=['POST'])  # 添加路由
def cssb():
    if request.method == 'POST':

        url = request.form.get('url')
        f = request.files['file']
        if url == '':
            if not (f and allowed_file(f.filename)):
                return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})
            user_input = request.form.get("name")
            basepath = os.path.dirname(__file__)  # 当前文件所在路径
            upload_path = os.path.join(basepath, 'static/picture',
                                       secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
            f.save(upload_path)
            path = 'static/picture/' + f.filename
            str1 = {}
            # print(len(chesunshibie.chesun(path)))
            str1 = damageIdentification.damageIdentification(path)
            # print(str1)
            str2 = [0 for i in range(len(str1))]
            for i in range(len(str1)):
                str2[i] = str1[i]
            print(str2)
            return render_template('index.html', cs="picture/" + str(f.filename), str1=str2, val1=time.time())
        else:
            base = url[0:21]
            if base.find("base64"):
                url64 = url[22:]
                basepath = os.path.dirname(__file__)
                imgdata = base64.b64decode(url64)
                name = "test" + '.png'
                path = 'static/picture/' + name
                file = open('static/picture/' + '/' + "test" + '.png', 'wb')
                file.write(imgdata)
                file.close()
                image = cv2.imread('static/picture/' + name)
                print(name)
                str1 = damageIdentification.damageIdentification(path)
                # print(str1)
                str2 = [0 for i in range(len(str1))]
                for i in range(len(str1)):
                    str2[i] = str1[i]
                print(str2)
                return render_template('index.html', cs="picture/" + str(f.filename), str1=str2, val1=time.time())
            else:
                filename = download_img(url)
                path = 'static/picture/' + filename
                basepath = os.path.dirname(__file__)
                image = cv2.imread('static/picture/' + filename)
                str1 = {}
                # print(len(chesunshibie.chesun(path)))
                str1 = damageIdentification.damageIdentification(path)
                # print(str1)
                str2 = [0 for i in range(len(str1))]
                for i in range(len(str1)):
                    str2[i] = str1[i]
                print(str2)
                return render_template('index.html', cs="picture/" + filename, str1=str2, val1=time.time())

#驾驶行为分析模块
@app.route("/jsxwfx", methods=['POST'])  # 添加路由
def jsxwfx():
    if request.method == 'POST':
        url = request.form.get('url')
        f = request.files['file']
        if url == '':
            if not (f and allowed_file(f.filename)):
                return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})
            user_input = request.form.get("name")
            basepath = os.path.dirname(__file__)  # 当前文件所在路径
            upload_path = os.path.join(basepath, 'static/picture',
                                       secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
            f.save(upload_path)
            path = 'static/picture/' + f.filename
            both_hands_leaving_wheel, eyes_closed, no_face_mask, not_buckling_up, smoke, cellphone, not_facing_front, yawning, head_lowered = drivingBehaviorAnalysis.drivingBehaviorAnalysis(
                path)

            return render_template('index.html', jsxwfx="picture/" + str(f.filename),
                                   both_hands_leaving_wheel=both_hands_leaving_wheel, eyes_closed=eyes_closed,
                                   no_face_mask=no_face_mask, not_buckling_up=not_buckling_up, smoke=smoke,
                                   cellphone=cellphone, not_facing_front=not_facing_front, yawning=yawning,
                                   head_lowered=head_lowered, val1=time.time())
        else:
            base = url[0:21]
            if base.find("base64"):
                url64 = url[22:]
                basepath = os.path.dirname(__file__)
                imgdata = base64.b64decode(url64)
                name = "test" + '.png'
                path = 'static/picture/' + name
                file = open('static/picture/' + '/' + "test" + '.png', 'wb')
                file.write(imgdata)
                file.close()
                image = cv2.imread('static/picture/' + name)
                print(name)
                both_hands_leaving_wheel, eyes_closed, no_face_mask, not_buckling_up, smoke, cellphone, not_facing_front, yawning, head_lowered = drivingBehaviorAnalysis.drivingBehaviorAnalysis(
                    path)

                return render_template('index.html', jsxwfx="picture/" + str(f.filename),
                                       both_hands_leaving_wheel=both_hands_leaving_wheel, eyes_closed=eyes_closed,
                                       no_face_mask=no_face_mask, not_buckling_up=not_buckling_up, smoke=smoke,
                                       cellphone=cellphone, not_facing_front=not_facing_front, yawning=yawning,
                                       head_lowered=head_lowered, val1=time.time())
            else:
                filename = download_img(url)
                path = 'static/picture/' + filename
                basepath = os.path.dirname(__file__)
                image = cv2.imread('static/picture/' + filename)
                both_hands_leaving_wheel, eyes_closed, no_face_mask, not_buckling_up, smoke, cellphone, not_facing_front, yawning, head_lowered = drivingBehaviorAnalysis.drivingBehaviorAnalysis(
                    path)

                return render_template('index.html', jsxwfx="picture/" + filename,
                                       both_hands_leaving_wheel=both_hands_leaving_wheel, eyes_closed=eyes_closed,
                                       no_face_mask=no_face_mask, not_buckling_up=not_buckling_up, smoke=smoke,
                                       cellphone=cellphone, not_facing_front=not_facing_front, yawning=yawning,
                                       head_lowered=head_lowered, val1=time.time())

#车辆属性识别模块
@app.route("/clsxsb", methods=['POST'])  # 添加路由
def clsxsb():
    if request.method == 'POST':
        url = request.form.get('url')
        f = request.files['file']
        if url == '':
            if not (f and allowed_file(f.filename)):
                return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})
            user_input = request.form.get("name")
            basepath = os.path.dirname(__file__)  # 当前文件所在路径
            upload_path = os.path.join(basepath, 'static/picture',
                                       secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
            f.save(upload_path)
            path = 'static/picture/' + f.filename

            # print(len(chesunshibie.chesun(path)))
            str1 = attributeIdentification.attributeIdentification(path)



            return render_template('index.html', clsxsb="picture/" + str(f.filename), str2=str1, val1=time.time())
        else:
            base = url[0:21]
            if base.find("base64"):
                url64 = url[22:]
                basepath = os.path.dirname(__file__)
                imgdata = base64.b64decode(url64)
                name = "test" + '.png'
                path = 'static/picture/' + name
                file = open('static/picture/' + '/' + "test" + '.png', 'wb')
                file.write(imgdata)
                file.close()
                image = cv2.imread('static/picture/' + name)
                print(name)
                str1 = attributeIdentification.attributeIdentification(path)

                return render_template('index.html', clsxsb="picture/" + str(f.filename), str2=str1, val1=time.time())
            else:
                filename = download_img(url)
                path = 'static/picture/' + filename
                basepath = os.path.dirname(__file__)
                image = cv2.imread('static/picture/' + filename)
                str1 = attributeIdentification.attributeIdentification(path)

                return render_template('index.html', clsxsb="picture/" +filename, str2=str1, val1=time.time())


@app.route('/')
def main():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
    # host='0.0.0.0', port=5000, debug=False
