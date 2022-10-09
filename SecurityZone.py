import numpy as np
from math import sqrt, pi


class SecurityZone(object):
    def __init__(self):
        self.width = 1024
        self.height = 1024
        self.R = 50
        self.hth = 20 # higher threshold, the more it is low, the less it is sensible
        self.lth = 2 # lesser threshold, the more it is high, the less it is sensible

    def mse(self, imA, imB):
        err = sqrt(np.sum((imA - imB)**2))
        err /= float(self.width*self.height)
        return err

    def comp_im(self, imA, imB):
        imdiff = abs(imA - imB)
        return imdiff

    def err_computing(self, framepack, dist, radius): #this function is only called on forks, no self.variables are modified
        FRAME_PACK_SIZE = len(framepack)
        im_ref = np.zeros(shape=(self.width, self.height))
        for i in range(FRAME_PACK_SIZE):
            print(i)
            im_ref += framepack[i]/(FRAME_PACK_SIZE-1)
        im_err = self.comp_im(im_ref, framepack[-1])
        err = self.mse(im_ref, framepack[-1])

        print(err)
        alert = self.secu_beholding(dist, radius, im_err)
        return alert

    def secu_beholding(self, dist, radius, im_err):
        X = []
        Y = []
        rad = radius*512/dist
        print(rad)
        for i in range(1, self.width-1): # avoid including the sides
            for j in range(1, self.height-1): # avoid including the sides
                # hysteresis thresholding loop
                if sqrt((i - 512) ** 2 + (j - 512) ** 2) <= rad:
                    if im_err[i, j] > self.hth: #something is moving there [i, j]
                        im_err[i, j] = 255
                    elif im_err[i, j] < self.lth: #nothing is moving there [i, j]
                        im_err[i, j] = 0
                    else:
                        hys = 0
                        for k in range(3):
                            for l in range(3):
                                if im_err[i-1+k, j-1+l] > self.hth:
                                    hys += 1
                                elif im_err[i-1+k, j-1+l] < self.lth:
                                    hys -= 1
                        if hys >= 2:
                            for k in range(3):
                                for l in range(3):
                                    im_err[i-1+k, j-1+l] = 255
                        elif hys <= -2:
                            for k in range(3):
                                for l in range(3):
                                    im_err[i-1+k, j-1+l] = 0
                else:
                    im_err[i, j] = 0
        for i in range(1, self.width-1): # avoid including the sides
            for j in range(1, self.height-1): # avoid including the sides
                if im_err[i, j] == 255:
                    X.append(i)
                    Y.append(j) #lists of coordinates that will be send to the MainLoop.py
        return X, Y
