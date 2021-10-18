import cv2 as cv
import numpy as np
import tkinter as tk


def Prog1():
    im = cv.imread('morf_test.png')

    img = cv.cvtColor(im, cv.COLOR_RGB2GRAY)

    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (120,120))

    tophat = cv.morphologyEx(img, cv.MORPH_TOPHAT, kernel)

    blackhat = cv.morphologyEx(tophat, cv.MORPH_BLACKHAT, kernel)


    ret, thresh = cv.threshold(blackhat, 60, 255, cv.THRESH_BINARY_INV)

    kernel2 = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3,3))
    eroded = cv.erode(thresh, kernel2, iterations=1)

    cv.imshow('input', im)
    cv.waitKey(0)

    cv.imshow('black_hat', blackhat)
    cv.waitKey(0)
    
    cv.imshow('top_hat', tophat)
    cv.waitKey(0)
    
    cv.imshow('eroded', eroded)
    cv.waitKey(0)

    cv.destroyAllWindows()

def Prog2():
    im = cv.imread('cookies.tif')
    ret, thresh = cv.threshold(im, 120, 255, cv.THRESH_BINARY)

    cv.imshow('input', im)
    cv.waitKey(0)
    cv.imshow('binary', thresh)
    cv.waitKey(0)

    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (7,7))
    closing = cv.morphologyEx(thresh, cv.MORPH_CLOSE, kernel)
    cv.imshow('closed', closing)
    cv.waitKey(0)

    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (118,118))
    opening = cv.morphologyEx(closing, cv.MORPH_OPEN, kernel)
    cv.imshow('opened', opening)
    cv.waitKey(0)

    im_out = cv.bitwise_and(im, opening)
    cv.imshow('subtracted', im_out)
    cv.waitKey(0)
    cv.destroyAllWindows()


def bwareaopen(img, min_size, connectivity):
        
        num_labels, labels, stats, centroids = cv.connectedComponentsWithStats(
            img, connectivity=connectivity)
        
        for i in range(num_labels):
            label_size = stats[i, cv.CC_STAT_AREA]
            
            if label_size < min_size:
                img[labels == i] = 0
                
        return img

def Prog3():
    im = cv.imread('img_cells.jpg')
    gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)

    ret, thresh = cv.threshold(gray, 120, 255, cv.THRESH_BINARY)

    cv.imshow('input', im)
    cv.waitKey(0)
    
    cv.imshow('binary', thresh)
    cv.waitKey(0)

    im_erode = cv.erode(thresh, kernel=(7,7), iterations=2)
    cv.imshow('eroded', im_erode)
    cv.waitKey(0)

    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3,3))
    opening = cv.morphologyEx(im_erode, cv.MORPH_OPEN, kernel)
    cv.imshow('opened', opening)
    cv.waitKey(0)

    im_out = bwareaopen(opening, 200, 8)
    cv.imshow('bwareopened', im_out)
    cv.waitKey(0)

    dilate = cv.dilate(im_out, kernel=(3,3), iterations=2)

    cv.imshow('dilated', dilate)
    cv.waitKey(0)

    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
    closed = cv.morphologyEx(dilate, cv.MORPH_CLOSE, kernel)

    cv.imshow('closed', closed)
    cv.waitKey(0)

    ret, inv = cv.threshold(closed, 70, 255, cv.THRESH_BINARY_INV)

    background = cv.dilate(inv, kernel=(3,3), iterations=2)
    cv.imshow('background', background)
    cv.waitKey(0)

    dist_transform = cv.distanceTransform(inv, cv.DIST_L2, 0)
    ret, foreground = cv.threshold(dist_transform, 0.1*dist_transform.max(), 255, 0)
    cv.imshow('foreground', foreground)
    cv.waitKey(0)

    foreground = np.uint8(foreground)
    unknow = cv.subtract(background, foreground)

    ret, markers = cv.connectedComponents(foreground)

    markers += 1

    markers[unknow==255] = 0

    markers = cv.watershed(im, markers)
    im[markers == -1] = [51, 255, 255]

    cv.imshow('output', im)
    cv.waitKey(0)
    cv.destroyAllWindows()

def Menu():
    root = tk.Tk()
    frame = tk.Frame(root)
    frame.pack()
    root.title("IIP Program")

    button_1 = tk.Button(frame,
                         text="Question 1",
                         height=2,
                         width=10,
                         fg="blue",
                         command=Prog1)
    button_1.pack(expand=100)
    button_1.pack(side=tk.LEFT)

    button_2 = tk.Button(frame,
                         text="Question 2",
                         height=2,
                         width=10,
                         fg="green",
                         command=Prog2)
    button_2.pack(side=tk.LEFT)
    button_2.pack(expand=10)

    button_2 = tk.Button(frame,
                         text="Question 3",
                         height=2,
                         width=10,
                         fg="purple",
                         command=Prog3)
    button_2.pack(side=tk.LEFT)
    button_2.pack(expand=10)

    button_3 = tk.Button(frame,
                         text="Quit",
                         height=2,
                         width=10,
                         fg="red",
                         command=quit)
    button_3.pack(side=tk.RIGHT)
    button_3.pack(expand=10)
    
    root.mainloop()    

# Graphical Interface
Menu()

# Separated Execution
# Prog1()
# Prog2()
# Prog3()
