import cv2

class CameraStream:
    def __init__(self, rtsp_url):
        self.cap = cv2.VideoCapture(rtsp_url)

    def is_connected(self):
        return self.cap.isOpened()

    def get_frame(self):
        ret, frame = self.cap.read()
        return frame if ret else None

    def release(self):
        self.cap.release()
