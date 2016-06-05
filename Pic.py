##############################################################################
#                           Pic.py
#            Represents the picture drawn on the screen
##############################################################################
from visual import *
# from PIL import Image
import cv2
import math
import numpy as np
from scipy.ndimage import interpolation
import scipy.misc


class Pic:
    def __init__(self, im, faces):
        self.faces = faces
        # Force to 2^n for VPython
        img = cv2.imread(im)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        height, width, channels = img.shape
        dim = max(width, height)
        exp = ceil(math.log(dim, 2))
        size = int(pow(2, exp))
        # Lets pad the image to the frame
        x = int((size - width) / 2.0)
        y = int((size - height) / 2.0)
        self.raw = cv2.copyMakeBorder(img, y, y, x, x,
                                      cv2.BORDER_CONSTANT, value=[1, 1, 1])
        self.img = self.raw
        self.size = size
        self.cut()
        # Set Properties of self

        # self.canny = cv2.Canny(self.raw, 50, 200)
        # self.raw = cv2.addWeighted(open_cv_image, 0.7, self.canny, 0.3, 0.3)

    def cut(self):
        # p = self.screen2im(pt)
        img = self.img
        mask = np.zeros(img.shape[:2], np.uint8)

        bgdModel = np.zeros((1, 65), np.float64)
        fgdModel = np.zeros((1, 65), np.float64)

        rect = (10, 10, 500, 500)
        cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5,
                    cv2.GC_INIT_WITH_RECT)

        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
        img = img * mask2[:, :, np.newaxis]
        # self.raw = img
        scipy.misc.imsave('mask.jpg', mask2 * 255)
        self.mask = mask2

    def findp2(self, p1):
        p1 = self.screen2im(p1)
        # print p1, self.mask.shape
        # Go from p1.x along y = p1.y
        mask = self.mask[p1[1], p1[0]:self.size - 1]
        foundOne = False
        for i in range(0, mask.shape[0] - 1):
            if foundOne == false and mask[i] == 1:
                foundOne = true
            if foundOne == true and mask[i] == 0:
                return self.im2screen([p1[0] + i, p1[1]])

    def findAlongY(self, pt):
        p1 = self.screen2im(pt)
        # print p1, self.mask.shape
        # Go from p1.x along y = p1.y
        mask = self.mask[p1[1]:self.size - 1, p1[0]]
        # print mask
        foundOne = False
        for i in range(0, mask.shape[0] - 1):
            if foundOne == false and mask[i] == 1:
                foundOne = true
            if foundOne == true and mask[i] == 0:
                return self.im2screen([p1[0], p1[1] + i])

    def closestEdge(self, pt, delta=2):
        """ Returns the closest edge at the pooint specified
        """
        d = 9999999
        pt = self.screen2im((int(pt[0]), int(pt[1])))
        closest = pt
        for i in range(pt[0] - delta, pt[0] + delta):
            for j in range(pt[1] - delta, pt[1] + delta):
                if (i >= 0 and j >= 0 and i < self.size and j < self.size and
                               self.canny[j, i] > 0):
                    dist = (i - pt[0]) ^ 2 + (j - pt[1]) ^ 2
                    if (dist < d):
                        d = dist
                        closest = (i, j)
        return self.im2screen(closest)

    def extract(self, ar, br):
        times = self.faces
        a = np.array(ar)
        b = np.array(br)
        diff = np.subtract(b, a)
        m = np.max(diff)
        op = np.zeros([a.shape[0], m, 3])
        im = np.array(self.img)
        for i in range(a.shape[0]):
            r1 = self.screen2im(a[i])
            r2 = self.screen2im(b[i])
            k = im[r1[1], r1[0]:r2[0]]
            interpolation.zoom(k, [float(m) / k.shape[0], 1],
                               output=op[i, :, :])
        exp = math.ceil(math.log(op.shape[1], 2))
        exp2 = math.ceil(math.log(op.shape[0], 2))
        zoomY = float(pow(2, exp)) / op.shape[1]
        zoomX = float(pow(2, exp2)) / op.shape[0]
        o = interpolation.zoom(op, [2 * zoomX, zoomY, 1])
        p = np.zeros([o.shape[0], o.shape[1] * times, o.shape[2]])
        for k in range(1, times + 1):
            if k % 2 == 0:
                p[:, (k - 1) * o.shape[1]:k * o.shape[1], :] = o
            else:
                p[:, (k - 1) * o.shape[1]:k * o.shape[1], :] = o[:, ::-1, :]
        p = np.roll(p, o.shape[1] / 2, 1)
        scipy.misc.imsave('temp.jpg', p)
        img = cv2.imread('temp.jpg')
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return img

    def im2screen(self, pt):
        return (pt[0] - self.size / 2, self.size / 2 - pt[1], 0)

    def screen2im(self, pt):
        return (pt[0] + self.size / 2, self.size / 2 - pt[1], 0)

    def topleft(self):
        m = self.mask #cv2.blur(self.mask, (2,2))
        loc = np.where(m == 1)
        return self.im2screen((loc[1][0], loc[0][0]))

    def closestLeft(self, pt):
        p1 = self.screen2im((int(pt[0]), int(pt[1])))
        # We are looking for the leftmost point
        # So we move right
        if self.mask[p1[1], p1[0]] == 0:
            # We are forced to move to the right
            for i in range(p1[0], self.size - 1):
                if self.mask[p1[1], i] == 1:
                    return self.im2screen((i, p1[1]))
        else:
            # We move left
            for i in range(p1[0], 0, -1):
                if self.mask[p1[1], i] == 0:
                    return self.im2screen((i + 1, p1[1]))

    def closestRight(self, pt):
        p1 = self.screen2im((int(pt[0]), int(pt[1])))
        # We are looking for the rightmost point
        # So we move left
        if self.mask[p1[1], p1[0]] == 0:
            # We are forced to move to the left
            for i in range(p1[0], 0, -1):
                if self.mask[p1[1], i] == 1:
                    return self.im2screen((i, p1[1]))
        else:
            # We move right
            for i in range(p1[0], self.size):
                if self.mask[p1[1], i] == 0:
                    return self.im2screen((i - 1, p1[1]))

    def closestInRow(self, pt, delta=10):
        """ Returns the closest edge at the point specified
        """
        pt = self.screen2im((int(pt[0]), int(pt[1]), 0))
        for i in range(0, 2):
            j = pt[0] - i
            if (j > 0 and self.canny[pt[1], j] > 0):
                return self.im2screen((j, pt[1], 0))
            k = pt[0] + i
            if (k < self.size and self.canny[pt[1], k] > 0):
                return self.im2screen((k, pt[1], 0))
        return self.im2screen(pt)

    def scaled(self, newSize):
        # c = cv2.merge((self.canny, self.canny, self.canny))
        # Set display image to be the overlayed version
        # im = cv2.addWeighted(self.raw, 0.9, c, 0.9, 0)
        im = self.raw
        return cv2.resize(im, (newSize, newSize),
                          interpolation=cv2.INTER_CUBIC)
