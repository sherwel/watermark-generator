#!/usr/bin/env python

try:
    from tkinter import Tk, Toplevel, Frame, Label, Scale, HORIZONTAL, Button, Entry, Menu
except ImportError:
    from Tkinter import Tk, Toplevel, Frame, Label, Scale, HORIZONTAL, Button, Entry, Menu

import tkFileDialog

from PIL import Image, ImageTk, ImageEnhance, ImageFont, ImageDraw
import sys


# textboxes to move watermark location
# but for black or white

class WaterMark(Frame):
    def __init__(self, master, image, image_name):
        Frame.__init__(self, master)
        self.image = image
        self.image_name = image_name

        # make a blank image for the text, initialized to transparent text color
        self.txt = Image.new('RGBA', self.image.size, (255,255,255,0))
        self.fnt = ImageFont.truetype('MontereyFLF.ttf', 50)
        self.d = ImageDraw.Draw(self.txt)

        self.name = "watermark"
        self.loc_x = 0
        self.loc_y = 225
        self.filler = (0,0,0,200)
        self.d.text((self.loc_x, self.loc_y), self.name, font=self.fnt, fill=self.filler)

        self.out = Image.alpha_composite(self.image, self.txt)
        self.tkim = ImageTk.PhotoImage(self.out)

        #display image
        Label(root, image=self.tkim).pack()

        # opacity scale
        s_opacity = Scale(self, label="Opacity", orient=HORIZONTAL, from_=0, to=255, resolution=1, command=self.update_opacity)
        s_opacity.set(200)
        s_opacity.pack(pady = 10)


        #update text
        self.textbox = Entry()
        self.textbox.pack(pady = 10)
        b_text = Button(master, text="update text", command=self.update_text)
        b_text.pack()

        b_color = Button(master, text="black/white", command=self.update_color)
        b_color.pack()
        
        b_save = Button(master, text="save image", command=self.save_image)
        b_save.pack()

    def update_color(self):    
        if self.filler[0] == 255:
            self.filler = (0,0,0,self.filler[3])
        else:
            self.filler = (255,255,255,self.filler[3])
        self.update()

    def update_text(self):
        self.name = self.textbox.get()
        self.update()

    def update_opacity(self, value):
        opacity = eval(value)
        self.filler = (self.filler[0],self.filler[1],self.filler[2],opacity)
        self.update()

    def update(self):
        self.txt = Image.new('RGBA', self.image.size, (255,255,255,0))
        self.fnt = ImageFont.truetype('MontereyFLF.ttf', 50)
        self.d = ImageDraw.Draw(self.txt)
        self.d.text((self.loc_x, self.loc_y), self.name, font=self.fnt, fill=self.filler)
        self.out = Image.alpha_composite(self.image, self.txt)
        self.tkim.paste(self.out)


    def save_image(self):
        #open original image
        im = Image.open(self.image_name).convert('RGBA')

        #get x and y location relative to original image using location
        #from thumbnail
        x = (self.loc_x / float(self.image.size[0])) * im.size[0]
        y = (self.loc_y / float(self.image.size[1])) * im.size[1]

        #same as in init
        txt = Image.new('RGBA', im.size, (255,255,255,0))
        fnt = ImageFont.truetype('MontereyFLF.ttf', im.size[1]/10)
        d = ImageDraw.Draw(txt)
        d.text((x,y), self.name, font=fnt, fill=self.filler)
        out = Image.alpha_composite(im, txt)

        out.save("watermark.jpg")


def openfile():

    image_name = tkFileDialog.askopenfilename(parent=root)
    im = Image.open(image_name).convert('RGBA')

    im.thumbnail((500, 500))

    WaterMark(root, im, image_name).pack()
    

####main
root = Tk()
root.wm_title("watermark generator")
root.geometry("800x1000")

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=openfile)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

root.config(menu=menubar)
root.mainloop()
