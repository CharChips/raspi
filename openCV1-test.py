import cv2
from picamera import Picamera2
piCam=Picamera2()
piCam.preview_configuration.main.size=(1280,720)
piCam.preview_configuration.main.format="RGB888"
piCam.preview_configuration.align()
piCam.configure("preview")
piCam.start()
while True:
  frame=piCam.capture_array()
  cv2.imshow("piCam" , frame)
  if cv2.waitkey(1)==ord('q'):
    break
cv2.destroyAllWindow()
