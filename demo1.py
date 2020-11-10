# Athanasios Theocharis
# AEM: 2961
# Digital Image Processing
# Assignment A 2020

import numpy as np
import cv2

############
# If you want the returned matrix to be the same dimension as A, then set dim = 'same'
# else set dim = ''
############
def myConv2(A_local, b_local, dim):
        Bwidth = b_local.shape[0]
        Bheight = b_local.shape[1]
        Awidth = A_local.shape[0]
        Aheight = A_local.shape[1]
        Cwidth = Awidth+Bwidth-1
        Cheight = Aheight+Bheight-1
        C = np.zeros((Cwidth, Cheight), dtype=int)
        midBx = Bwidth / 2
        midBy = Bheight / 2
        output = np.zeros((Cwidth, Cheight), dtype=int)
        pad = int((Cwidth - Awidth)/2)
        if Bwidth%2==1:
            C[pad:-pad, pad:-pad] = A_local
        else:
            pad +=1
            if pad == 1:
                C[1:, 1:]=A_local
            else:
                C[pad:-pad+1, pad:-pad+1] = A_local

        for i in range(Cwidth):
            for j in range(Cheight):
                for k in range(Bwidth):
                    for m in range(Bheight):
                        reverKernelRow = Bwidth - 1 - k
                        reverseKernelCol = Bheight - 1 - m
                        newPositionX = int(i + (midBy - reverKernelRow))
                        newPositionY = int(j + (midBx - reverseKernelCol))
                        if 0 <= newPositionX < Cwidth and 0 <= newPositionY < Cheight:
                            output[i][j] += C[newPositionX][newPositionY] * b_local[reverKernelRow][reverseKernelCol]
        if dim=='same':
            if pad == 1:
                return output[1:, 1:]
            else:
                return output[pad:-pad + 1, pad:-pad + 1]
        return output


def myImNoise(A_local, noise):
    if noise == 'gaussian':
        height = A_local.shape[0]
        width = A_local.shape[1]
        gauss_noise = np.random.normal(5, 10, A_local.shape)
        for i in range(height):
            for j in range(width):
                newValue = A_local[i][j] + gauss_noise[i][j]
                if newValue > 255:
                    A_local[i][j] = 255
                else:
                    A_local[i][j] = newValue
        return A_local
    elif noise == 'saltandpepper':
        height = A_local.shape[0]
        width = A_local.shape[1]
        for i in range(height):
            for j in range(width):
                if int(10*np.random.random()) == 1: #10% SNR
                    if int(2*np.random.random()) == 1:
                        A_local[i][j] = 255
                    else:
                        A_local[i][j] = 0
    return A_local


def myImFilter(A_local, filter, size):
    if filter == 'median':
        kernelX = size
        kernelY = size
        window = np.zeros((kernelX*kernelY), dtype=int)
        newA = np.zeros((A_local.shape[0],A_local.shape[1]), dtype=int)
        midWindowX = int(kernelX / 2)
        midWindowY = int(kernelY / 2)
        for x in range(midWindowX, A_local.shape[0] - midWindowX):
            for y in range(midWindowY, A_local.shape[1] - midWindowY):
                index = 0
                for winX in range(0, kernelX):
                    for winY in range(0, kernelY):
                        window[index] = A_local[x + winX - midWindowX - 1][y + winY - midWindowY - 1]
                        index += 1
                window = np.sort(window)
                value = window[int(kernelX*kernelY/2)]
                newA[x][y] = value
        return np.uint8(newA)
    elif filter == 'mean':
        b = np.ones((size, size), np.float32) / (size*size)
        convoluted = myConv2(A_local, b, 'same')
        height = convoluted.shape[0]
        width = convoluted.shape[1]
        for i in range(height):
            for j in range(width):
                if convoluted[i][j] > 255:
                    convoluted[i][j] = 255
        return np.uint8(convoluted)


contin = 1
while contin == 1:
    A = cv2.imread('test.png', 0)  # read image - black and white
    cv2.imshow('image', A)  # show image
    cv2.waitKey(0)  # wait for key press
    cv2.destroyAllWindows()  # close image window
    val = 0
    while val != 1 and val != 2:
        val = int(input("Press 1 if you want to choose Gaussian noise or 2 if you want to choose saltandpepper noise\n"))
    size = 0

    if val == 1:
        B = myImNoise(A, 'gaussian')
    else:
        B = myImNoise(A, 'saltandpepper')
    cv2.imshow('image', B)  # show image
    cv2.waitKey(0)  # wait for key press
    cv2.destroyAllWindows()  # close image window
    while size < 2:
        size = int(input("Please enter filter size larger than 1. You should enter one number, since it's going to be square\n"))

    val = 0
    while val != 1 and val != 2:
        val = int(input("Press 1 if you want to choose Mean Filter or 2 if you want to choose Median Filter\n"))
    if val == 1:
        C = myImFilter(B, 'mean', size)
    else:
        C = myImFilter(B, 'median', size)
    cv2.imshow('image', C)  # show image
    cv2.waitKey(0)  # wait for key press
    cv2.destroyAllWindows()  # close image window
    contin = int(input("If you want to continue press 1\n"))
