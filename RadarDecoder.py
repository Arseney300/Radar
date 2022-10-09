from RadarListener import *
import math

class RadarDecoder(object):
    def RenderCordinates(self, angleraw, angle, framecount, lastdrawnangle, oldangle):
        imgw = 1024
        imgh = 1024
        midx = 512
        midy = 512
        framecount+=1
        if (framecount > 5):
            x1 = midx + math.cos(math.radians(lastdrawnangle)) * 512
            y1 = midy + math.cos(math.radians(lastdrawnangle)) * 512
            x2 = midx + math.cos(math.radians(oldangle + 1)) * 512
            y2 = midy + math.cos(math.radians(oldangle + 1)) * 512

            minx = max(min(x1, x2, midx) - 1, 0)
            miny = max(min(y1, y2, midy) - 1, 0)
            maxx = min(max(x1, x2, midx) + 1, imgw)
            maxy = min(max(y1, y2, midy) + 1, imgh)

            lastdrawnangle = oldangle
            framecount = 0

        rad = math.radians(angle)
        radcos = math.cos(rad)
        radsin = math.sin(rad)
        return midx, radcos, midy, radsin, lastdrawnangle, oldangle

    def Cordinates(self, lineHeader):
        angleraw = (lineHeader[9]&0xff)<<8 | (lineHeader[8]&0xff)
        # rr = lineHeader[23]&0xff
        # sstt = (lineHeader[13]&0xff)<<8|(lineHeader[12]&0xff)
        # meter = sstt*10/math.sqrt(2)
        angle=angleraw*360/4096 - 90
        return angleraw, angle
