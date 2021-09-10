import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import tkinter as tk


def is_gray(input_img):
    if len(input_img.shape) < 3:
        return True


def dec_int(input_im):
    if not is_gray(input_im):
        decreased_im = split_and_decrease(input_im)
        increased_im = split_and_increase(decreased_im)
    else:
        decreased_im = decrease_im_size(input_im)
        increased_im = increase_im_size(decreased_im)

    cv.imshow('Decimated Reduction', decreased_im)
    cv.waitKey(0)
    cv.imshow('Decimated Interpolation', increased_im)
    cv.waitKey(0)
    cv.destroyAllWindows()


def split_and_decrease(input_im):
    r, g, b = cv.split(input_im)

    r1 = decrease_im_size(r)
    g1 = decrease_im_size(g)
    b1 = decrease_im_size(b)
    out_im = np.dstack((r1, g1, b1))
    return out_im


def split_and_increase(input_im):
    r, g, b = cv.split(input_im)

    r1 = increase_im_size(r)
    g1 = increase_im_size(g)
    b1 = increase_im_size(b)
    out_im = np.dstack((r1, g1, b1))
    return out_im


def decrease_im_size(channel):
    res_ch = []
    for i in range(len(channel)):
        for j in range(len(channel[0])):
            if i % 2 == 0 and j % 2 == 0:
                aux = channel[i][j]
                res_ch.append(aux)

    res_ch = np.array(res_ch)
    width = int(len(channel) / 2)
    height = int(len(channel[0]) / 2)
    dim = (width, height)
    res_ch = np.reshape(res_ch, dim)

    return res_ch


def increase_im_size(channel):
    res_ch = []
    aux = []
    for i in range(len(channel)):
        if len(aux) != 0:
            for elem in range(len(aux)):
                res_ch.append(aux[elem])

            aux.clear()
        for j in range(len(channel[0])):
            if i % 2 == 0 and j % 2 == 0:
                res_ch.append(channel[i][j])
                aux.append(channel[i][j])
                res_ch.append(channel[i][j])
                aux.append(channel[i][j])

            if i % 2 == 0 and j % 2 == 1:
                res_ch.append(channel[i][j])
                aux.append(channel[i][j])
                res_ch.append(channel[i][j])
                aux.append(channel[i][j])

            if i % 2 == 1 and j % 2 == 0:
                res_ch.append(channel[i][j])
                aux.append(channel[i][j])
                res_ch.append(channel[i][j])
                aux.append(channel[i][j])

            if i % 2 == 1 and j % 2 == 1:
                res_ch.append(channel[i][j])
                aux.append(channel[i][j])
                res_ch.append(channel[i][j])
                aux.append(channel[i][j])
    if len(aux) != 0:
        for elem in range(len(aux)):
            res_ch.append(aux[elem])
        aux.clear()

    res_ch = np.array(res_ch)
    width = len(channel) * 2
    height = len(channel[0]) * 2
    dim = (width, height)
    res_ch = np.reshape(res_ch, dim)

    return res_ch


def edge_improv(input_im, imp_type):
    laplacian = None
    k_vert_hori = np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]])
    k_diagonal = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])
    if imp_type == 1:
        kernel = k_vert_hori
        laplacian = 'Vertical and Horizontal'
    else:
        kernel = k_diagonal
        laplacian = 'Diagonal'

    if not is_gray(input_im):
        r, g, b = cv.split(input_im)

        r_filtered = cv.filter2D(r, -1, kernel)
        g_filtered = cv.filter2D(g, -1, kernel)
        b_filtered = cv.filter2D(b, -1, kernel)

        out_im = np.dstack((r_filtered, g_filtered, b_filtered))
    else:
        out_im = cv.filter2D(input_im, -1, kernel)

    improved_im = cv.add(input_im, out_im)

    cv.imshow('Laplacian : {}'.format(laplacian), improved_im)
    cv.waitKey(0)
    cv.destroyAllWindows()


def average_improv(input_im, num):
    kernel = np.ones((num, num), np.int16) * 1 / pow(num, 2)
    if not is_gray(input_im):
        r, g, b = cv.split(input_im)
        filtered_r = cv.filter2D(r, -1, kernel)
        filtered_g = cv.filter2D(g, -1, kernel)
        filtered_b = cv.filter2D(b, -1, kernel)
        filtered_im = np.dstack((filtered_r, filtered_g, filtered_b))
    else:
        filtered_im = cv.filter2D(input_im, -1, kernel)

    edges_im = cv.subtract(input_im, filtered_im)
    improved_im = cv.add(input_im, edges_im)

    cv.imshow('Dif Average filter - Factor {}'.format(num), improved_im)
    cv.waitKey(0)
    cv.destroyAllWindows()


def bicubic_decrease(input_im):
    width = int(input_im.shape[1] / 2)
    height = int(input_im.shape[0] / 2)
    dim = (width, height)
    im_output = cv.resize(input_im, dim, interpolation=cv.INTER_CUBIC)

    return im_output


def bicubic_increase(input_im):
    width = int(input_im.shape[1] * 2)
    height = int(input_im.shape[0] * 2)
    dim = (width, height)
    im_output = cv.resize(input_im, dim, interpolation=cv.INTER_CUBIC)

    return im_output


def cv_interpolation(input_im):
    decreased_im = bicubic_decrease(input_im)
    increased_im = bicubic_increase(decreased_im)

    # cv.imshow('Bicubic Reduction', decreased_im)
    # cv.waitKey(0)
    # cv.imshow('Bicubic Interpolation', increased_im)
    # cv.waitKey(0)
    # cv.destroyAllWindows()
    return decreased_im


def cv_interpolation_2(input_im):
    decreased_im = bicubic_decrease(input_im)
    increased_im = bicubic_increase(decreased_im)

    return increased_im


def gamma_correction(input_im, gamma):
    equalized_im = np.uint8(pow((input_im / 255), gamma) * 255)

    cv.imshow(' Gamma Correction factor: {}'.format(gamma), equalized_im)
    cv.waitKey(0)
    cv.destroyAllWindows()


def histogram_equalization(input_im):
    if not is_gray(input_im):
        r, g, b = cv.split(input_im)
        r1 = cv.equalizeHist(r)
        g1 = cv.equalizeHist(g)
        b1 = cv.equalizeHist(b)

        histogram_equalized_im = np.dstack((r1, g1, b1))
    else:
        histogram_equalized_im = cv.equalizeHist(input_im)

    cv.imshow('Histogram Equalization', histogram_equalized_im)
    cv.waitKey(0)
    cv.destroyAllWindows()


def histogram_equalization2(input_im):
    if not is_gray(input_im):
        r, g, b = cv.split(input_im)
        r1 = cv.equalizeHist(r)
        g1 = cv.equalizeHist(g)
        b1 = cv.equalizeHist(b)

        histogram_equalized_im = np.dstack((r1, g1, b1))
    else:
        histogram_equalized_im = cv.equalizeHist(input_im)

    return histogram_equalized_im


def histogram_plot(input_im):
    if not is_gray(input_im):
        r, g, b = cv.split(input_im)
        plt.hist(r.ravel(), 256, [0, 256])
        plt.hist(g.ravel(), 256, [0, 256])
        plt.hist(b.ravel(), 256, [0, 256])

        plt.title('RGB Histogram')
        plt.show()
    else:
        plt.hist(input_im.ravel(), 256, [0, 256])
        plt.title('Grayscale Histogram')
        plt.show()


def im_calculate_CDF(input_im):
    if not is_gray(input_im):
        r, g, b = cv.split(input_im)

        count, bins_count = np.histogram(input_im, bins=255)
        pdf = count / sum(count)
        cdf1 = np.cumsum(pdf)

        count2, bins_count = np.histogram(input_im, bins=255)
        pdf = count2 / sum(count2)
        cdf2 = np.cumsum(pdf)

        count3, bins_count = np.histogram(input_im, bins=255)
        pdf = count3 / sum(count3)
        cdf3 = np.cumsum(pdf)

        cdf = (cdf1 + cdf2 + cdf3) / 3
    else:
        count, bins_count = np.histogram(input_im, bins=255)
        pdf = count / sum(count)
        cdf = np.cumsum(pdf)

    plt.plot(cdf)
    plt.title('CDF')
    plt.show()


def gaussian_smoothing(input_im, size, sigma):
    smooth_image = cv.GaussianBlur(input_im, (size, size), sigma)

    cv.imshow(f'Smooth image - Sigma: {sigma} - gaussian_size: {size}x{size}', smooth_image)
    cv.waitKey(0)
    # cv.destroyWindow(smooth_image)
    return smooth_image


def Prog1():
    im = cv.imread('test80.jpg')
    cv.imshow('Original', im)
    cv.waitKey(0)
    # cv.destroyAllWindows()
    dec_int(im)
    im_2 = cv_interpolation(im)
    im_3 = cv_interpolation_2(im)
    # average_improv(im, 5)
    edge_improv(im_2, 1)
    edge_improv(im_3, 1)


def Prog2():
    im1 = cv.imread('car.png', 0)
    im2 = cv.imread('crowd.png', 0)
    im3 = cv.imread('university.png', 0)
    cv.imshow('Original', im1)
    cv.waitKey(0)
    # cv.destroyAllWindows()
    gamma_correction(im1, 1.5)
    gamma_correction(im1, 3.0)
    gamma_correction(im1, 6.0)
    gamma_correction(im1, 0.75)
    gamma_correction(im1, 0.5)
    gamma_correction(im1, 0.25)
    histogram_equalization(im1)
    im1_1 = histogram_equalization2(im1)
    histogram_plot(im1)
    histogram_plot(im1_1)
    im_calculate_CDF(im1)
    im_calculate_CDF(im1_1)

    cv.imshow('Original', im2)
    cv.waitKey(0)
    gamma_correction(im2, 1.5)
    gamma_correction(im2, 3.0)
    gamma_correction(im2, 6.0)
    gamma_correction(im2, 0.75)
    gamma_correction(im2, 0.5)
    gamma_correction(im2, 0.25)
    histogram_equalization(im2)

    cv.imshow('Original', im3)
    cv.waitKey(0)
    gamma_correction(im3, 1.5)
    gamma_correction(im3, 3.0)
    gamma_correction(im3, 6.0)
    gamma_correction(im3, 0.75)
    gamma_correction(im3, 0.5)
    gamma_correction(im3, 0.25)
    histogram_equalization(im3)


def Prog3():
    im = cv.imread('Image1.pgm')
    cv.imshow('Original', im)
    cv.waitKey(0)
    edge_improv(im, 2)
    smooth_image = gaussian_smoothing(im, 3, 0.5)
    edge_improv(smooth_image, 1)
    smooth_image2 = gaussian_smoothing(im, 3, 1.0)
    edge_improv(smooth_image2, 1)
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


Menu()

