import cv2

class CameraStream:
    def __init__(self, rtsp_url):
        self.cap = cv2.VideoCapture(rtsp_url)

    def is_connected(self):
        try:
            if self.cap.isOpened():
                return True
            else:
                print(f"[ERROR] No se pudo establecer conexión con la cámara")
                return False
        except Exception as e:
            print(f"[ERROR] No se pudo establecer conexión con la cámara: {e}")
            return False

    def get_frame(self):
        ret, frame = self.cap.read()
        return frame if ret else None

    def release(self):
        self.cap.release()
