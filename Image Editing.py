import sys
import cv2
import easygui
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import *
from tkinter import messagebox

root = tk.Tk()
root.geometry('700x700')
root.title('Choose to convert !!')
root.configure(background='light blue')
label = Label(root, background="black", font=("arial",30,"bold"))

def u():
    Imagepath = easygui.fileopenbox()
    c(Imagepath)

def c(Imagepath):
    originalimage = cv2.imread(Imagepath)
    originalimage = cv2.cvtColor(originalimage, cv2.COLOR_BGR2RGB)

    if originalimage is None:
        print("Can not find out any image !!!")
        sys.exit()

    R_1 = cv2.resize(originalimage, (930, 510))

    greyScaleImage = cv2.cvtColor(originalimage, cv2.COLOR_BGR2GRAY)
    R_2 = cv2.resize(greyScaleImage, (930, 510))

    smoothGrayScale = cv2.medianBlur(greyScaleImage, 5)
    R_3 = cv2.resize(smoothGrayScale, (930, 510))

    getEdgeImage = cv2.adaptiveThreshold(smoothGrayScale, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    R_4 = cv2.resize(getEdgeImage, (930, 510))

    colorImage = cv2.bilateralFilter(originalimage, 9, 300,300)
    R_5 = cv2.resize(colorImage, (930, 510))

    cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=getEdgeImage)
    R_6 = cv2.resize(cartoonImage, (930, 510))

    images = [R_1, R_2, R_3, R_4, R_5, R_6]

    fig,axes =plt.subplots(3,2, figsize=(8,8), subplot_kw={'xticks':[], 'yticks': []}, gridspec_kw= dict(hspace=0.1, wspace=0.1))

    for i,ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap = 'gray')
    
    save1 = Button(root, text=" Save Grey Scale Image ", command= lambda : save(R_2,Imagepath), padx=20, pady=5)
    save1.configure(background="red", foreground="yellow", font=('arial', 10, "bold"))
    save1.pack(side=TOP, pady=25)

    save2 = Button(root, text=" Save Smooth Image ", command= lambda : save(R_3,Imagepath), padx=20, pady=5)
    save2.configure(background="red", foreground="yellow", font=('arial', 10, "bold"))
    save2.pack(side=TOP, pady=25)

    save3 = Button(root, text=" Save Edge Image ", command= lambda : save(R_4,Imagepath), padx=20, pady=5)
    save3.configure(background="red", foreground="yellow", font=('arial', 10, "bold"))
    save3.pack(side=TOP, pady=25)

    save4 = Button(root, text=" Save Colour Image ", command= lambda : save(R_5,Imagepath), padx=20, pady=5)
    save4.configure(background="red", foreground="yellow", font=('arial', 10, "bold"))
    save4.pack(side=TOP, pady=25)

    save5 = Button(root, text=" Save Cartoon Image ", command= lambda : save(R_6,Imagepath), padx=20, pady=5)
    save5.configure(background="red", foreground="yellow", font=('arial', 10, "bold"))
    save5.pack(side=TOP, pady=25)

    plt.show()

def save(ReSized6, Imagepath):
    newname= "Converted Image ..."
    path1 = os.path.dirname(Imagepath)
    extension = os.path.splitext(Imagepath)[1]
    path = os.path.join(path1, newname + extension)
    cv2.imwrite(path, cv2.cvtColor(ReSized6, cv2.COLOR_RGB2BGR))
    I = " The save image is of the name " + newname + " at " + path
    tk.messagebox.showinfo(title = None, message =I)

a = Button(root, text=" Conversion of Image ", command= u, padx=15, pady=10)
a.configure(background="black", foreground="white", font=("arial",30,"bold"))
a.pack(side=TOP, pady=50)

root.mainloop()
