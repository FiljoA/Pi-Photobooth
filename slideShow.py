import mtTkinter as tk
from PIL import Image, ImageTk
import os
import time
from random import randint

class slideShow(tk.Toplevel):
    def __init__(self, debug, *args, **kwargs):
	tk.Toplevel.__init__(self, *args, **kwargs)

	self.debug = debug

	if self.debug == True:
	    print('Debug Mode')

	#Get toplevel; Remove window decoration
	self.win = args[0]
	self.win.wm_geometry("0x0+0+0")
	#Merge slideshow with toplevel
	self.overrideredirect(True)

	#The slideshow widget, holds images
        self.label = tk.Label(self)
        self.label.focus_set()
        #self.label.pack(side="top", fill="both", expand=True)
	self.label.grid(row=0, column=0)

	#Clicking slideshow give toplevel focus
        self.label.bind("<Button-1>", self.getFocus)

	#Used to save images in RAM
	#Avoid garbage collection
	self.persistent_image = None

	#slideshow size
	scr_w, scr_h = self.winfo_screenwidth(), self.winfo_screenheight()
	self.img_w, self.img_h = scr_w, scr_h
	if self.debug == True:
		self.img_w /= 2
		self.img_h /= 2
	self.imgSize = self.img_w, self.img_h
	#center window
	self.center_w, self.center_h = (scr_w/2 - self.img_w/2), (scr_h/2 - self.img_h/2)
	self.wm_geometry("{}x{}+{}+{}".format(self.img_w-4, self.img_h-1, self.center_w, self.center_h))

	self.imageList = []

    def getFocus(self, event):
        self.win.focus_force()
	if self.debug == True:
	    print('Clicked')

    def showBG(self, dir):
	blackIMG = Image.open(dir + "black.JPG")
	blackIMG = blackIMG.resize(self.imgSize)
	self.persistent_image = ImageTk.PhotoImage(blackIMG)
	self.label.configure(image=self.persistent_image)
	self.update()
	self.oldImg = blackIMG

    def getImages(self, dir):
        for root, dirs, files in os.walk(dir):
            for f in files:
                if f.endswith(".png") or f.endswith(".jpg"):
                    img_path = os.path.join(root, f)
                    self.imageList.append(img_path)

    def updateImage(self, dir):
	self.getImages(dir)
	image = self.imageList[randint(0, len(self.imageList)) - 1]
	self.showImage(image, True)
	#self.win.after(1000, self.win.main)

    def showImage(self, filename, transition):
	self.alpha = 1.0
        image = Image.open(filename)  
        image = image.resize(self.imgSize)
	if transition == True:
        	self.transition(image)
	if transition == False:
		self.persistent_image = ImageTk.PhotoImage(image)
		self.label.configure(image=self.persistent_image)
		self.update()
        self.oldImg = image

    def transition(self, newImg):
        self.alpha = 0.0
	image = Image.blend(self.oldImg, newImg, self.alpha)
        while 1.00 >= self.alpha:
            image = Image.blend(self.oldImg, newImg, self.alpha)

            #create new image
            self.persistent_image = ImageTk.PhotoImage(image)
            self.label.configure(image=self.persistent_image)

            #update label
            self.update()
            time.sleep(0.008)
            self.alpha += 0.2