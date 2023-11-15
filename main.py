import cv2
import easygui
import numpy as np
import imageio
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image

app=tk.Tk()
app.geometry('400x400')
app.title('Cartoonify Your Image !')
app.configure(background='blue')
label=Label(app,background='#CDCDCD', font=('calibri',20,'bold'))

def upload():
    ImagePath=easygui.fileopenbox()
    cartoonify(ImagePath)

def cartoonify(ImagePath):
    orginalimage  = cv2.imread(ImagePath)
    orginalimage = cv2.cvtColor(orginalimage, cv2.COLOR_BGR2RGB)

    if orginalimage is None:
        print("Can not find any image.")
        sys.exit()

    resize = cv2.resize(orginalimage, (960, 540))

    grayScaleImage = cv2.cvtColor(orginalimage, cv2.COLOR_BGR2GRAY)
    resize2 = cv2.resize(grayScaleImage, (960, 540))

    smoothGrayScale = cv2.medianBlur(grayScaleImage, 5)
    resize3 = cv2.resize(smoothGrayScale, (960,540))

    getEdge = cv2.adaptiveThreshold(smoothGrayScale, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    resize4 = cv2.resize(getEdge, (960, 540))

    colorImage = cv2.bilateralFilter(orginalimage, 9, 300, 300)
    resize5 = cv2.resize(colorImage, (960, 540))

    cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=getEdge)
    resize6 = cv2.resize(cartoonImage, (960, 540))

    images = [resize, resize2, resize3, resize4, resize5, resize6]

    fig, axes = plt.subplots(3, 2, figsize=(8, 8), subplot_kw={'xticks': [], 'yticks': []},
                             gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')

    save_image = Button(app, text="Save cartoon image", command=lambda: save(resize6, ImagePath), padx=30, pady=5)
    save_image.configure(background='#364156', foreground='white', font=('calibri', 10, 'bold'))
    save_image.pack(side=TOP, pady=50)

    plt.savefig("image.png")
    plt.close()

def save(ReSized6, ImagePath):
    newName="cartoonified_Image"
    path1 = os.path.dirname(ImagePath)
    extension=os.path.splitext(ImagePath)[1]
    path = os.path.join(path1, newName+extension)
    cv2.imwrite(path, cv2.cvtColor(ReSized6, cv2.COLOR_RGB2BGR))
    I= "Image saved by name " + newName +" at "+ path
    tk.messagebox.showinfo(title=None, message=I)


upload=Button(app,text="Cartoonify an Image",command=upload,padx=10,pady=5)
upload.configure(background='#364156', foreground='white',font=('calibri',10,'bold'))
upload.pack(side=TOP,pady=50)

app.mainloop()