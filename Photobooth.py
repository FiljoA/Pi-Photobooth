import slideShow as slideWidget
import camera as camModule
import mtTkinter as tk
from mtTkinter import *
import RPi.GPIO as GPIO
from collections import namedtuple

#Config
#light  - GPIO pin
#switch - GPIO pin 23
#delay  - How long to show image
#dir    - Where to store images
#debug  - Make slideshow smaller

struct = namedtuple("struct", "light switch effectSwitch delay dir debug")

class Photobooth(tk.Tk):
    def __init__(self, config):
	tk.Tk.__init__(self)

	#Setup GPIO
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(config.light, GPIO.OUT)
	GPIO.output(config.light, False)
	GPIO.setup(config.effectSwitch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(config.switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)

	#Setup slideshow and camera
	self.slideShow = slideWidget.slideShow(config.debug, self)
	self.camera = camModule.camera()
	self.effect = 'none'

	#Events
	#Using the callback parameter creates a new thread which can make things slower and glitchy
	GPIO.add_event_detect(config.switch, GPIO.RISING, bouncetime=3000)
	GPIO.add_event_detect(config.effectSwitch, GPIO.RISING, bouncetime=3000)

	#Timer used in mainloop, delays are handled in the slideshow class
	self.t = 0

	#Show black background
	self.slideShow.showBG(config.dir)

	#Used to show text on top of image
	self.oText = tk.Label(self.slideShow)
	self.updateLabel('Photobooth v3.0')
	
	#start psuedo main loop
	self.main()

    def main(self):
	#Poll events
	if GPIO.event_detected(config.switch) == True:
		self.takeAndShowPic()
		#Reset timer when picture is taken
		#This delays the slideshow
		self.t = 0
	if GPIO.event_detected(config.effectSwitch) == True:
		self.changeEffect()

	#Update slideShow after delay
	if self.t >= 1000 * config.delay:
		self.slideShow.updateImage(config.dir)
		self.t = 0

	self.t += 1
	self.after(0, self.main)

    def updateLabel(self, string):
	self.oText.configure(text=str(string))
	self.oText.grid(row=0, column=0, sticky='s')	
	self.update()
	self.after(3000, self.hideLabel)

    def hideLabel(self):
	print('cleared')
	self.oText.grid_forget()
	self.update()

    def changeEffect(self, event = 0):
	if self.effect == 'cartoon':
		self.effect = 'none'	
	elif self.effect == 'none':
		self.effect = 'cartoon'

	if config.debug == True:
		print('Effect changed')
	#Display text that effect has changed
	#self.oText.configure(text='Effect: ' + self.effect)
	self.updateLabel('Effect: ' + self.effect)
	#self.after(2000, self.m.destroy())

    def takeAndShowPic(self, event = 0):
	if config.debug == True:
		print('Effect: ' + self.effect)
	GPIO.output(config.light, True)
	self.slideShow.showBG(config.dir)
	#takePic returns filename of taken picture
	filename = self.camera.takePic(config.dir, self.effect)
	self.slideShow.showImage(filename, False)
	self.effect = 'none'
	GPIO.output(config.light, False)

    def quit(self):
	GPIO.cleanup()
	self.destroy()

config = struct(light = 18, switch = 23, effectSwitch = 12, delay = 10, dir = "/home/pi/RoboticSugar/Photobooth-Pics/", debug = True)

photobooth = Photobooth(config)
photobooth.bind("<Escape>", lambda e: photobooth.quit()) #Quit
photobooth.mainloop()