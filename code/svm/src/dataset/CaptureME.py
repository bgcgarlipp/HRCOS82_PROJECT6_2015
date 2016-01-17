#!/usr/bin/python

import subprocess
import Tkinter as tk
import cv2
from PIL import Image, ImageTk

capture = False
lastImage = ""

width, height = 1280, 720
cap = cv2.VideoCapture(0)

root = tk.Tk()
root.bind('<Escape>', lambda e: root.quit())

lblDetailsText = tk.StringVar()
blbAUDetails = tk.Label(root, textvariable=lblDetailsText)
blbAUDetails.pack(side = tk.TOP)
lblDetailsText.set("Click Button to estimate AU")

lmain = tk.Label(root)

def captureAU():
    global capture
    capture = True

Button1 = tk.Button(root, text = "Capture AU", command = captureAU)
Button1.pack(side = tk.BOTTOM)

lmain = tk.Label(root)
lmain.pack()

def show_frame():
    global capture
    _, frame = cap.read()
#     frame = cv2.flip(frame, 1)

    # Save Image to disk
    if capture:
        capture = False
        cv2.imwrite("predictAU/image.jpg", frame)
        getImageEstimate()
    
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)

def getImageEstimate():
    try:
        proc = subprocess.Popen(['python', 'parseAU.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = proc.communicate()[0].split(",")
        auDisplayed = []
        for au in output:
            values = au.split(":") 
            if values[1] == "1":
                auDisplayed.append( values[0] )
        lblDetailsText.set("AU Found: {}".format(auDisplayed))
    except Exception as  e:
        lblDetailsText.set("Image could not be processed")
    root.update_idletasks()
    pass

# TypeError: CvArr argument 'image' must be IplImage, CvMat or CvMatND. Use fromarray() to convert numpy arrays to CvMat or cvMatND
show_frame()

root.mainloop()
