import cv2
import RPi.GPIO as GPIO
import time 

print("OpenCV Version : ", cv2.__version__)

class MultiCamera:
    def __init__(self, selectPin=18, oePin=17, size=(240, 320)):
        self.selectPin = selectPin
        self.oePin = oePin
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.selectPin, GPIO.OUT)
        GPIO.setup(self.oePin, GPIO.OUT)
        # default disable FSA642
        GPIO.output(self.oePin, GPIO.HIGH)

        # camera configuration 
        self.config = [
                {'name' : 'Camera 1', 'select' : GPIO.LOW}, 
                {'name' : 'Camera 2', 'select' : GPIO.HIGH}
                ]

        # initialize camera
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, size[1])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, size[0])
        self.imgs = []

        # enable FSA642
        GPIO.output(self.oePin, GPIO.LOW)
    
    def capture(self):
        # capture from Camera
        self.imgs = []
        for conf in self.config :
            if self.cap.isOpened():
                ___, ___ = self.cap.read() # just for warming up 
                ret, img = self.cap.read()
                GPIO.output(self.selectPin, conf['select'])
                if not ret : 
                    raise Exception("failed to get image from %s" % conf['name'])
                self.imgs.append(img)

        return self.imgs

    def close(self):
        # disable camera
        self.cap.release()

        # disable FSA642
        GPIO.output(self.oePin, GPIO.HIGH)

if __name__ == "__main__" : 
    multi_camera = MultiCamera(selectPin=18, oePin=17, size=(240, 320))

    while True :
        # capture camera
        imgs = multi_camera.capture()
        
        # display camera
        img = cv2.hconcat(imgs)
        cv2.imshow("result", img)
        if ord('q') == cv2.waitKey(10):
            break
    cv2.destroyAllWindows()

    # close camera
    multi_camera.close()
