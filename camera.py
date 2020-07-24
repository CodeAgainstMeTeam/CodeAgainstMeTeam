'''
author:尹迎春
create time:2020-07-10
update time:2020-07-12
'''

#新功能需要、暂时舍弃

import cv2


class VideoCamera:
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def make_photo(self):
        """使用opencv拍照"""
        cap = cv2.VideoCapture(0)  # 默认的摄像头
        while True:
            ret, frame = cap.read()
            if ret:
                cv2.imshow("capture", frame)  # 弹窗口
                # 等待按键q操作关闭摄像头
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    # os.remove( './static/images/test.jpg' )
                    file_name = "./static/picture/test.jpg"
                    cv2.imwrite(file_name, frame)

                    break
            else:
                break
        cap.release()
        cv2.destroyAllWindows()
