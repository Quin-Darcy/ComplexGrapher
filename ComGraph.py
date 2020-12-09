import numpy as np
from PIL import Image
import cv2
import math
import cmath
import colorsys

def mult(x,y,z):
    arr = [[math.sqrt(3)/2, 0, 1/2], [-math.sqrt(2)/4, math.sqrt(2)/2, math.sqrt(6)/4], [-math.sqrt(2)/4, -math.sqrt(2)/2, math.sqrt(6)/4]]

    vec = [x, y, z]
    newv = [0, 0, 0]

    for i in range(3):
        for j in range(3):
            newv[i] += int(vec[j] * arr[i][j])      
    return newv


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
    

def Color_Function(a,b,w,h,rel,dr,iml,di,ans):
    c = a
    a = rel+a*(dr/w)
    b = iml+b*(di/h)
    t = complex(a,b)
    parr = [0,0,0]
    nz = 10**(-50)
    z = complex(0,0)
    if (c%2 == 0):
        c = 1
    else:
        c = -1
    if (t**5 == 0):
        parr = [255,255,255]
    else:
        z = 1/(t**(c*a))
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


def Color(ans):
    mx = int(input("\nEnter Max Image Length: "))
    Re = input("Enter Re range: ")
    Im = input("Enter Im range: ")
    Re = Re.split(" ", 1)
    Im = Im.split(" ", 1)
    rel = float(Re[0])
    reu = float(Re[1])
    iml = float(Im[0])
    imu = float(Im[1])
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
    size = (w,h)

    im = Image.new("RGB", size, 0)
    pixels = im.load()
    
    for y in range(h):
        for x in range(w):
            pixels[x,y] = Color_Function(x,y,w,h,rel,dr,iml,di,ans)
            
    im.save('COLOR.png')


def Img_Function(a,b,w,h,rel,dr,iml,di):
    c = a
    d = b
    a = rel+a*(dr/w)
    b = iml+b*(di/h)
    t = complex(a,b)
    i = complex(0,1)
    parr = [0,0,0]
    nz = 10**(-50)
    z = complex(0,0)
    if (cmath.sin(t) == 0):
        return[-1,-1]
    else:
        z = 1/cmath.sin(t)
        
    u = z.real
    v = z.imag

    u = int((u-rel)/(dr/w))
    v = int((v-iml)/(di/h))

    return [u,v]
    

def Img(ans):
    n = 0
    indx = [0,0]
    mx = int(input("\nEnter Max Image Length: "))
    Re = input("Enter Re range: ")
    Im = input("Enter Im range: ")
    Re = Re.split(" ", 1)
    Im = Im.split(" ", 1)
    rel = float(Re[0])
    reu = float(Re[1])
    iml = float(Im[0])
    imu = float(Im[1])
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
    size = (w,h)

    im = Image.open("test3.jpg")
    w2,h2 = im.size
    img = Image.new("RGB", size, 0)
    px = img.load()
    pixels = im.load()
    
    for y in range(h):
        for x in range(w):
            indx = Img_Function(x,y,w,h,rel,dr,iml,di)
            if (indx == [-1,-1]):
                px[x,y] = (0,0,0)
            px[x,y] = pixels[indx[0]%w2, indx[1]%h2]
        
    img.save('IMAGE.png')


def CB_Function(a,b,w,h,rel,dr,iml,di):
    a = rel+a*(dr/w)
    b = iml+b*(di/h)
    t = complex(a,b)
    i = complex(0,1)
    parr = [0,0,0]
    nz = 10**(-50)
    z = complex(0,0)
    if (t**2+t+1 == 0):
        return [0,0,0]
    else:
        z = (t-1)/(t**2+t+1)
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
        
    return tuple(parr)


def ChkrBrd(ans):
    n = 0
    mx = int(input("\nEnter Max Image Length: "))
    Re = input("Enter Re range: ")
    Im = input("Enter Im range: ")
    Re = Re.split(" ", 1)
    Im = Im.split(" ", 1)
    rel = float(Re[0])
    reu = float(Re[1])
    iml = float(Im[0])
    imu = float(Im[1])
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
    size = (w,h)

    img = Image.new("RGB", size, 255)
    px = img.load()
    
    for y in range(h):
        for x in range(w):
            px[x,y] = CB_Function(x,y,w,h,rel,dr,iml,di)  

    img.save('CHKRBRD.png')


def main():
    ans = int(input("\rSelect Graph Type\n1. Phase Portrait\n2. Phase Portrait with Modulus Contour Lines\n3. Phase Portrait with Phase Contour Lines\n4. Phase Portrain with Modulus and Phase Lines\n5. Phase Portrait with Checkerboard Tiling\n6. Photo Based\n7. Checkerboard\n\nSelection: "))

    if (1 <= ans <= 5):    
        Color(ans)
    elif (ans == 6):
        Img(ans)
    elif (ans == 7):
        ChkrBrd(ans)


main()
