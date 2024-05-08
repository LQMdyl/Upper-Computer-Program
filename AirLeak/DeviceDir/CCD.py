import cv2
from pylibdmtx import pylibdmtx
import numpy

class Camera():
    #初始化
    def __init__(self):
        self.Isconnect = False
        print("CCD init")

    #寻找摄像头
    def find_camera(self,index):
        try:
            camera = cv2.VideoCapture(index)
            return camera
        except Exception as e:
            return None

    #读取摄像头
    def read_camera(self, camera):
        #读取摄像头
        ret, frame = camera.read()
        return ret, frame

    #显示摄像头
    def show_camera(self, frame):
        #显示摄像头
        cv2.imshow('frame', frame)
    #关闭摄像头
    def close_camera(self, camera):
        #关闭摄像头
        camera.release()
        cv2.destroyAllWindows()

    #圈出图中的眼睛
    def circle_eye(self, frame):
        #圈出图中的眼睛
        eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in eyes:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        self.show_camera(frame)


    #在图上指定位置写字
    def write_text(self,X,Y, frame, text):
        #在图上指定位置写字
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, text, (X, Y), font, 1, (255, 255, 255), 1, cv2.LINE_AA)

    #圈出图片中的人脸
    def circle_face(self, frame):
        #圈出图片中的人脸
        face_cascade =cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            self.write_text(x, y, frame,"gts-test")
        self.show_camera(frame)

    #识别图中二维码
    def find_qrcode(self, frame):
        image=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        #二值化
        #ret, image = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY)
        all_barcode_info = pylibdmtx.decode( image, timeout=500, max_count=1 )

        Barcode=""
        if len(all_barcode_info)>0:
            self.write_text(0, 50, image, str(all_barcode_info[0].data.decode()))
            Barcode=str(all_barcode_info[0].data.decode())
        else:
            self.write_text(0, 50, image, "No Barcode")
            Barcode="No Barcode"

        #保存图片
        cv2.imwrite("test.jpg", image)
        return Barcode

    def Save_picture(self, frame):
        cv2.imwrite("test.jpg", frame)

    #摄像头主程序
    def main(self, camera):
        while True:
            ret, frame = self.read_camera(camera)
            self.show_camera(frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.close_camera(camera)

if __name__ == '__main__':
    camera = Camera()
    camera1 = camera.find_camera(1)
    ret, picture = camera.read_camera(camera1)
    if ret:
        barcode = camera.find_qrcode(picture)
        print(barcode)
    camera.main(camera1)

