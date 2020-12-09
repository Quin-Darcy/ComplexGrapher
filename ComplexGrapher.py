from tkinter import * 
from tkinter.ttk import *
import numpy as np
from PIL import Image
import tkinter as tk
from PIL import ImageTk
import cv2
import math
import cmath
import os
import time 
from tkinter import filedialog
os.system('clear')

#============================================================Inverse Matrix===========================================================

def mult(x,y,z):
    arr = [[math.sqrt(3)/2, 0, 1/2], [-math.sqrt(2)/4, math.sqrt(2)/2, math.sqrt(6)/4], [-math.sqrt(2)/4, -math.sqrt(2)/2, math.sqrt(6)/4]]

    vec = [x, y, z]
    newv = [0, 0, 0]

    for i in range(3):
        for j in range(3):
            newv[i] += int(vec[j] * arr[i][j])      
    return newv

#=============================================================Angle to Cube==========================================================

def setColor(t, mp, cont):
    arr = [0,0,0]
    k = (math.pi)/3
    a = math.sqrt(3)
    theta = (math.pi/2)-np.arccos(a/3)
    r = (127.5)*math.sqrt(3)
    c = r*a
    if (0<= t < k):
        x = c/(math.tan(t)+a)
        y = math.tan(t)*x
        z = (-(1/r)*2*x+2)*255*(math.sqrt(2)*math.sin(theta)-1/2)+127.5
        arr = mult(x,y,z)
    if (k<= t < 2*k):
        x = c/(2*math.tan(t))
        y = math.tan(t)*x
        z = -(1/r)*(x-r/2)*255*(1/2-math.sqrt(2)*math.sin(theta))+255*math.sqrt(2)*math.sin(theta)
        arr = mult(x,y,z)
    if (2*k<= t < 3*k):
        x = c/(math.tan(t)-a)
        y = math.tan(t)*x
        z = -(1/r)*(2*x+r)*255*(math.sqrt(2)*math.sin(theta)-1/2)+127.5
        arr = mult(x,y,z)
    if (3*k<= t < 4*k):
        x = -c/(math.tan(t)+a)
        y = math.tan(t)*x
        z = (1/r)*(2*x+2*r)*255*(1/2-math.sqrt(2)*math.sin(theta))+255*math.sqrt(2)*math.sin(theta)
        arr = mult(x,y,z)
    if (4*k<= t < 5*k):
        x = -c/(2*math.tan(t))
        y = math.tan(t)*x
        z = (1/r)*(x+r/2)*255*(math.sqrt(2)*math.sin(theta)-1/2)+127.5
        arr = mult(x,y,z)
    if (5*k <= t < 6*k):
        x = -c/(math.tan(t)-a)
        y = math.tan(t)*x
        z = (1/r)*(2*x-r)*255*(1/2-math.sqrt(2)*math.sin(theta))+255*math.sqrt(2)*math.sin(theta)
        arr = mult(x,y,z)

    if (cont != 0):
        for d in range(3):
            arr[d] = int(arr[d]*(mp)+arr[d]*(1-mp)/4)
        
    return arr
    

def Color_Function(a,b,w,h,rel,dr,iml,di,ans,fEntry):
    a = rel+a*(dr/w)
    b = iml+b*(di/h)
    t = complex(a,b)
    parr = [0,0,0]
    nz = 10**(-50)
    z = complex(0,0)

    try:
        f = eval("lambda z:" + fEntry)
    except NameError:
        return [-1,-1,-1]

    try:
        z = f(t)
    except ZeroDivisionError:
        parr = [255,255,255]
    except ValueError:
        parr = [105,105,105]
    except OverflowError:
        parr = [105,105,105]
    except NameError:
        return [-1,-1,-1]
    if (ans == 1):
        theta=(-cmath.phase(z)+2*math.pi)%(2*math.pi)
        parr = setColor(theta, 1, 0)
    elif (ans == 2):
        theta=(-cmath.phase(z)+2*math.pi)%(2*math.pi)
        q = abs(z)+nz
        p = math.log(q, 1.3)
        mod = 1-(math.ceil(p) - p)
        parr = setColor(theta, mod, 1) 
    elif (ans == 3):  
        theta=(-cmath.phase(z)+2*math.pi)%(2*math.pi)
        ph = 1-(math.ceil(theta%(math.pi/12))-theta%(math.pi/12))
        parr = setColor(theta, ph*5, 1) 
    elif (ans == 4):
        theta=(-cmath.phase(z)+2*math.pi)%(2*math.pi)
        q = abs(z)+nz
        p = math.log(q, 1.3)
        mod = 1-(math.ceil(p) - p)
        ph = 1-(math.ceil(theta%(math.pi/12))-theta%(math.pi/12))
        parr = setColor(theta, ph*mod*8, 1) 
    elif (ans == 5):
        theta=(-cmath.phase(z)+2*math.pi)%(2*math.pi)
        q = abs(z)+nz
        p = math.log(q, 1.3)
        mod = 1-(math.ceil(p) - p)
        ph = 1-(math.ceil(theta%(math.pi/12))-theta%(math.pi/12))
        num = math.ceil(theta/(math.pi/12))

        if ((math.ceil(p)%2 == 0 and num%2 == 0) or (math.ceil(p)%2 == 1 and num%2 == 1)):
            parr = [0,0,0]
        else:   
            parr = setColor(theta, ph*mod*9, 1)
    
    return tuple(parr)


def Color(ans, Entries):
    err = Image.new("RGB", (0,0), 255)
    mx = Entries[5]
    rel = Entries[1]
    reu = Entries[2]
    iml = Entries[3]
    imu = Entries[4]
    dr = abs(reu-rel)
    di = abs(imu-iml)
    if (dr >= di):
        w = mx
        ratio = di/dr
        h = int(ratio*w)
    else:
        h = mx
        ratio = dr/di
        w = int(ratio*h)
    try:
        size = (w,h)
        im = Image.new("RGB", size, 255)
        pixels = im.load()
    except ValueError:
        return [False,err]
    
    for y in range(h):
        for x in range(w):
            if (Color_Function(x,y,w,h,rel,dr,iml,di,ans,Entries[0]) == [-1,-1,-1]):
                return [False,err]
            else:
                pixels[x,y] = Color_Function(x,y,w,h,rel,dr,iml,di,ans,Entries[0])
            
    return [True, im]

def Img_Function(a,b,w,h,rel,dr,iml,di,ffEntry):
    a = rel+a*(dr/w)
    b = iml+b*(di/h)
    t = complex(a,b)

    try:
        f = eval("lambda z:" + ffEntry)
    except NameError:
        return [math.pi,math.pi]

    try:
        z = f(t)
    except ZeroDivisionError:
        z = complex(10000000000,10000000000)
    except ValueError:
        return [-1,-1]
    except OverflowError:
        return [-1,-1]
    except NameError:
        return [math.pi,math.pi]

    u = z.real
    v = z.imag

    u = int((u-rel)/(dr/w))
    v = int((v-iml)/(di/h))

    return [u,v]
    

def Img(ans, Entries):
    err = Image.new("RGB", (0,0), 255)
    indx = [0,0]
    mx = Entries[5]
    rel = Entries[1]
    reu = Entries[2]
    iml = Entries[3]
    imu = Entries[4]
    dr = abs(reu-rel)
    di = abs(imu-iml)
    if (dr >= di):
        w = mx
        ratio = di/dr
        h = int(ratio*w)
    else:
        h = mx
        ratio = dr/di
        w = int(ratio*h)
    try:
        size = (w,h)
        img = Image.new("RGB", size, 255)
        px = img.load()
    except ValueError:
        return [False,err]

    if (Entries[7] != ''):
        im = Image.open(Entries[7])
        w2,h2 = im.size
        pixels = im.load()
    else:
        return [False, err]
    
    for y in range(h):
        for x in range(w):
            indx = Img_Function(x,y,w,h,rel,dr,iml,di,Entries[0])
            if (indx == [-1,-1]):
                px[x,y] = (0,0,0)
            elif (indx == [math.pi,math.pi]):
                return [False,err]
            px[x,y] = pixels[indx[0]%w2, indx[1]%h2]

    return [True,img]

def CB_Function(a,b,w,h,rel,dr,iml,di,ffEntry):
    a = rel+a*(dr/w)
    b = iml+b*(di/h)
    t = complex(a,b)
    parr = [0,0,0]
    nz = 10**(-50)
    z = complex(0,0)
    try:
        f = eval("lambda z:" + ffEntry)
    except NameError:
        return [-1,-1,-1]
    
    try:
        z = f(t)
        q = abs(z)+nz
        p = math.log(q, 1.2)
        mod = (math.ceil(p) - p)   
        theta=(-cmath.phase(z)+2*math.pi)%(2*math.pi)       
        ph = (math.ceil(theta%(math.pi/18))-theta%(math.pi/18))
        num = math.ceil(theta/(math.pi/18))

        if ((math.ceil(p)%2 == 0 and num%2 == 0) or (math.ceil(p)%2 == 1 and num%2 == 1)):
            parr = [0,0,0]
        else:
            parr = [255,255,255]
    except ZeroDivisionError:
        parr = [255,255,255]
    except ValueError:
        parr = [105,105,105]
    except OverflowError:
        parr = [105,105,105]
    except NameError:
        return[-1,-1,-1]
        
    return tuple(parr)


def ChkrBrd(ans, Entries):
    n = 0
    err = Image.new("RGB", (0,0), 255)
    mx = Entries[5]
    rel = Entries[1]
    reu = Entries[2]
    iml = Entries[3]
    imu = Entries[4]
    dr = abs(reu-rel)
    di = abs(imu-iml)
    if (dr >= di and dr != 0):
        w = mx
        ratio = di/dr
        h = int(ratio*w)
    elif (di != 0):
        h = mx
        ratio = dr/di
        w = int(ratio*h)
    else:
        return [False, err]
    try:
        size = (w,h)
        img = Image.new("RGB", size, 255)
        px = img.load()
    except ValueError:
        return [False, err]
    
    for y in range(h):
        for x in range(w):
            if (CB_Function(x,y,w,h,rel,dr,iml,di,Entries[0]) != [-1,-1,-1]):
                px[x,y] = CB_Function(x,y,w,h,rel,dr,iml,di,Entries[0]) 
            else:
                return [False,err]

    return [True, img]


def main():
    img = Image.new("RGB", (0,0), 255)
    val = [True, img] 
    try:
        Entries = [str(fEntry.get()),float(RelEntry.get()),float(ReUEntry.get()),float(ImlEntry.get()),float(ImuEntry.get()),int(MaxEntry.get()),int(GraphEntry.get())+1,str(filename)]
    except ValueError:
        return [False, img]
    except NameError:
        Entries = [str(fEntry.get()),float(RelEntry.get()),float(ReUEntry.get()),float(ImlEntry.get()),float(ImuEntry.get()),int(MaxEntry.get()),int(GraphEntry.get())+1,'']

    if (1 <= Entries[6] <= 5):    
        val = Color(Entries[6], Entries)
    elif (Entries[6] == 6):
        val = Img(Entries[6], Entries)
    elif (Entries[6] == 7):
        val = ChkrBrd(Entries[6], Entries)
    
    return val



root = tk.Tk()
root.title("Complex Grapher")

#============================================================Canvas===========================================================

cnvs =tk.Canvas(root, width=2400, height=1400, bg='gray')
cnvs.grid(row=0,column=0,rowspan=19,columnspan=6, sticky='N')

#============================================================Frames===========================================================

mainFrame = tk.Frame(root, width=300, height=150, bg='gray')
mainFrame.grid(row=0,column=0,sticky='N')

imgFrame = tk.Frame(root, width=1000, height=1000, bg='gray', bd=10, relief=RIDGE)
imgFrame.grid(row=0,column=2, sticky='E')

errorFrame = tk.Frame(mainFrame,width=200, height=100, bg='gray')
errorFrame.grid(row=19,column=1)

#============================================================Labels===================================================================

fLabel = tk.Label(mainFrame,text="Enter Complex Function",bg='gray')
fLabel.grid(row=0,column=0,pady=7, sticky='W')

fLabel2 = tk.Label(mainFrame, text="f(z) = ",bg='gray')
fLabel2.grid(row=1,column=0, sticky='E')

ReLabel = tk.Label(mainFrame, text="Enter Re range",bg='gray')
ReLabel.grid(row=2, column=0,pady=7,sticky='W')

ReLlabel = tk.Label(mainFrame, text="Inf = ",bg='gray')
ReLlabel.grid(row=3,column=0,sticky='E')

ReUlabel = tk.Label(mainFrame, text="Sup = ",bg='gray')
ReUlabel.grid(row=4,column=0,sticky='E')

ImLabel = tk.Label(mainFrame, text="Enter Im range",bg='gray')
ImLabel.grid(row=5, column=0,pady=7,sticky='W')

ImLlabel = tk.Label(mainFrame, text="Inf = ",bg='gray')
ImLlabel.grid(row=6,column=0,sticky='E')

ImUlabel = tk.Label(mainFrame, text="Sup = ",bg='gray')
ImUlabel.grid(row=7,column=0,sticky='E')

MaxLabel = tk.Label(mainFrame, text="Enter MAX Image Length",bg='gray')
MaxLabel.grid(row=8, column=0,sticky='W')

GraphLabel = tk.Label(mainFrame, text="Select Graph Type: ",bg='gray')
GraphLabel.grid(row=10, column=0,sticky='W')

#============================================================Entries====================================================================

fEntry = tk.Entry(mainFrame, font=20)
fEntry.grid(row=1, column=1, pady=7)

RelEntry = tk.Entry(mainFrame, font=20)
RelEntry.grid(row=3,column=1,pady=7)

ReUEntry = tk.Entry(mainFrame, font=20)
ReUEntry.grid(row=4,column=1,pady=7)

ImlEntry = tk.Entry(mainFrame, font=20)
ImlEntry.grid(row=6,column=1,pady=7)

ImuEntry = tk.Entry(mainFrame, font=20)
ImuEntry.grid(row=7,column=1,pady=7)

MaxEntry = tk.Entry(mainFrame, font=20)
MaxEntry.grid(row=8,column=1,pady=64)

GraphEntry = IntVar()

Selections = ["Color","Color with Moduli Contour Lines","Color with Phase Contour Lines","Color with Moduli/Phase Contour Lines",
                        "Color with Checkerboard","Photo Based","Checkerboard"]

for val, Selections in enumerate(Selections):
    tk.Radiobutton(mainFrame,text=Selections,font=30,variable=GraphEntry,value=val, bg='gray').grid(row=11+val, column=1, sticky='W')

#===========================================================Functions===================================================================

def Clear():
    fEntry.delete(0,last=100)
    fEntry.insert(0,"")
    RelEntry.delete(0, last=100)
    RelEntry.insert(0,"")
    ReUEntry.delete(0, last=100)
    ReUEntry.insert(0,"")
    ImlEntry.delete(0, last=100)
    ImlEntry.insert(0,"")
    ImuEntry.delete(0, last=100)
    ImuEntry.insert(0,"")
    MaxEntry.delete(0, last=100)
    MaxEntry.insert(0,"")
    errorFrame.destroy()
    label.destroy()

def UploadAction(event=None):
    global filename
    filename = filedialog.askopenfilename()
    fileLabel = tk.Label(mainFrame, text=str(filename), font=20,bg='gray')
    fileLabel.grid(row=9,column=1)

def savefile(img):
    filen = filedialog.asksaveasfile(mode='w', defaultextension=".jpg")
    if not filen:
        return
    img.save(filen)

def newSize(s):
    arr = [0,0]
    arr[0] = s[0]
    arr[1] = s[1]
    if (arr[0] <= 1000 and arr[1] <= 1000):
        return s
    else:
        if (arr[0] >= arr[1]):
            r = arr[1]/arr[0]
            arr[0] = 1000
            arr[1] = int(arr[0]*r)
        else:
            r = arr[0]/arr[1]
            arr[1] = 1000
            arr[0] = int(arr[1]*r)
    return tuple(arr)


progress = Progressbar(root, orient = HORIZONTAL, length = 500, mode = 'determinate') 

def bar(): 
    progress['value'] = 20
    root.update_idletasks() 
    time.sleep(1) 
  
    progress['value'] = 40
    root.update_idletasks() 
    time.sleep(1) 
  
    progress['value'] = 50
    root.update_idletasks() 
    time.sleep(1) 
  
    progress['value'] = 60
    root.update_idletasks() 
    time.sleep(1) 
  
    progress['value'] = 80
    root.update_idletasks() 
    time.sleep(1)
    val = main()
    progress['value'] = 90
    if (not val[0]):
        errorLabel = tk.Label(errorFrame, text="INVALID ENTRY",font=('Helvetica', 40, 'bold'), bg='gray',fg='red')
        errorLabel.grid(row=19,column=1) 
    else:
        size = newSize(val[1].size)
        temp = val[1].resize(size, Image.ANTIALIAS)
        photo2 = ImageTk.PhotoImage(temp)
        global label
        label = Label(imgFrame,image=photo2)
        label.image=photo2
        label.grid(row=0,column=2)
        saveButton = tk.Button(mainFrame, font=30, text="SAVE",command=lambda: savefile(val[1]))
        saveButton.grid(row=21,column=1,pady=10, sticky='E')

    progress['value'] = 100
  
progress.grid(pady = 10) 
    
#============================================================Buttons=====================================================================

UploadButton = tk.Button(mainFrame, font=30, text="Upload",command=UploadAction)
UploadButton.grid(row=9,column=0,pady=7, sticky='E')

submitButton = tk.Button(mainFrame, font=30, text="GRAPH",command=bar)
submitButton.grid(row=20,column=1,pady=7, sticky='E')

clearButton = tk.Button(mainFrame, font=30, text="CLEAR", command=Clear)
clearButton.grid(row=20,column=0,pady=7)

root.mainloop()


