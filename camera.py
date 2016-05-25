import picamera
import time

class camera():
    def __init__(self):
	#Setup camera
	self.camera = picamera.PiCamera()
	#16:9  - 2592 x 1458
	# 4:3  - 2592 x 1944
	self.camera.resolution = (1600, 900)
	self.camera.framerate = 15

    def takePic(self, dir, effect, event = 0):
	self.camera.image_effect = effect
	self.camera.start_preview()

	#camera timer
	t = 3
	while t > 0:
		self.camera.annotate_text = str(t)
		t -= 1
		time.sleep(0.5)

	self.camera.annotate_text = 'Smile!'
	time.sleep(0.5)
	self.camera.annotate_text = ''

	#Get time for file name
	timeStamp = str(time.time())
	filename = dir + timeStamp + 'pb3.jpg'

	self.camera.capture(filename)
	self.camera.stop_preview()

	return filename