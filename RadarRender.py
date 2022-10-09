import pygame
from pygame.locals import *
from RadarListener import *
from SecurityZone import *
from math import sqrt
import numpy as np


class RadarRender(object):
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((1024, 1024))
        pygame.display.set_caption("Radar")
        self.surf = pygame.Surface((1024, 1024))
        self.distance = ['50', '75', '100', '250', '500', '750', '1000', '1500', '2000', '3000', '4000', '6000', '8000', '12000', '16000', '24000']
        self.speed = 'slow: 24rpm' #initial value
        self.range = 100  # initial value (as in MainLoop.py)
        self.security_radius = 50

        ##########HIGHLIGHT AND RADIUS############
        self.bold = False
        self.radius = 100
        self.displayradius = False
        ###########################################

        ###############DISTANCE DRAG###############
        self.x_init = 512
        self.y_init = 512
        self.xf = 512
        self.yf = 512
        ###########################################

        ###############SPEED INFO##################
        self.font3 = pygame.font.Font(None, 32)
        self.font3.set_italic(True)
        ###########################################

        #############RANGE BOX#####################
        self.font = pygame.font.Font(None, 28)
        self.font.set_italic(True)
        self.range_box = pygame.Rect(864, 72, 56, 20)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.colortextrange = self.color_inactive
        self.activetextrange = False
        self.text = 'range in meters' #default text
        ###########################################

        #############SECURITY RADIUS################
        self.font4 = pygame.font.Font(None, 28)
        self.font4.set_italic(True)
        self.sec_rad_box = pygame.Rect(864, 96, 56, 20)
        self.colorsecrad = self.color_inactive
        self.activesecrad = False
        self.rad_text = 'security radius'  # default text

        self.on_rect = pygame.Rect(864, 120, 26, 18)
        self.off_rect = pygame.Rect(894, 120, 34, 18)
        self.coloron = self.color_active
        self.coloroff = self.color_inactive
        ###########################################

        #############RANGE MENU#####################
        self.font2 = pygame.font.Font(None, 20)
        Y_RANGE_SIZE = 20
        X_RANGE_SIZE = 56
        BOX_NB = 16
        self.font2.set_italic(True)

        self.rangemenu = [None]*BOX_NB
        for i in range(BOX_NB):
            self.rangemenu[i] = pygame.Rect(8+int(i/8)*X_RANGE_SIZE, 8+(i%8)*Y_RANGE_SIZE, X_RANGE_SIZE, Y_RANGE_SIZE)

        self.color = [self.color_inactive]*BOX_NB
        self.color[2] = self.color_active
        ###########################################

    def InitSpeed(self, s):
        self.speed = s #initial value

    def ColorAct(self, event):
        BOX_NB = 16
        if self.range_box.collidepoint(event.pos):
            if self.text == 'enter a range':
                self.text = ''
            else:
                self.activetextrange = not self.activetextrange
            self.text = ''
        else:
            self.activetextrange = False
        self.colortextrange = self.color_active if self.activetextrange else self.color_inactive
        ###########################################
        if self.sec_rad_box.collidepoint(event.pos):
            if self.rad_text == 'enter a range':
                self.rad_text = ''
            else:
                self.activesecrad = not self.activesecrad
            self.rad_text = ''
        else:
            self.activesecrad = False
        self.colorsecrad = self.color_active if self.activesecrad else self.color_inactive
        ###########################################
        for k in range(BOX_NB):
            if self.rangemenu[k].collidepoint(event.pos):
                for i in range(BOX_NB):
                    self.color[i] = self.color_inactive
                self.color[k] = self.color_active
                self.range = int(self.distance[k])
                RadarListener().Distance(self.range)

        if self.on_rect.collidepoint(event.pos):
            self.coloron = self.color_active
            self.coloroff = self.color_inactive
        if self.off_rect.collidepoint(event.pos):
            self.coloroff = self.color_active
            self.coloron = self.color_inactive

    def ChangeSpeed(self, key):
        if key == 113: #K_q
            self.speed = 'quick: 36rpm'
            RadarListener().ScanSpeed('quick')
        elif key == 120: #K_x
            self.speed = 'bolting: 48rpm'
            RadarListener().ScanSpeed('bolting')
        else: # K_s
            self.speed = 'slow: 24rpm'
            RadarListener().ScanSpeed('slow')

    def TextRangeCircle(self, event):
        if self.activetextrange:
            if event.key == K_RETURN:
                try:
                    self.radius = int(self.text)
                    if self.radius <= self.range:
                        self.displayradius = True
                except ValueError:
                    self.text = 'enter a range'
                    self.displayradius = False
            if event.key == K_KP_ENTER:
                try:
                    if self.radius <= self.range:
                        self.radius = int(self.text)
                        self.displayradius = True
                except ValueError:
                    self.text = 'enter a range'
                    self.displayradius = False
            elif event.key == K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                try:
                    num = int(event.unicode)
                    self.text += str(num)
                except ValueError:
                    self.text += ''

    ###########################################
    def TextSecuRadius(self, event):
        if self.activesecrad:
            if event.key == K_RETURN:
                try:
                    self.security_radius = int(self.rad_text)
                except ValueError:
                    self.rad_text = 'enter a range'
            if event.key == K_KP_ENTER:
                try:
                    self.security_radius = int(self.rad_text)
                except ValueError:
                    self.rad_text = 'enter a range'
            elif event.key == K_BACKSPACE:
                self.rad_text = self.rad_text[:-1]
            else:
                try:
                    num = int(event.unicode)
                    self.rad_text += str(num)
                except ValueError:
                    self.rad_text += ''
        ###########################################

    def ScaleRange(self, key):
        BOX_NB = 16
        if key == 273:
            if self.range > int(self.distance[0]):
                self.range = int(self.distance[self.distance.index(str(self.range)) - 1])
                RadarListener().Distance(self.range)
                for i in range(BOX_NB):
                    self.color[i] = self.color_inactive
                self.color[self.distance.index(str(self.range))] = self.color_active
                self.DrawCircles()
        elif key == 274:
            if self.range < int(self.distance[15]):
                self.range = int(self.distance[self.distance.index(str(self.range)) + 1])
                RadarListener().Distance(self.range)
                for i in range(BOX_NB):
                    self.color[i] = self.color_inactive
                self.color[self.distance.index(str(self.range))] = self.color_active
                self.DrawCircles()

    def Frame(self, LineData, midx, radcos, midy, radsin, x_a, y_a): #
        for i in range(512):
            x = midx + radcos * i
            y = midy + radsin * i
            l = LineData[i]
            self.surf.fill((l, l, l), (x, y, 1, 1))
        self.surf.fill((255, 64, 64), (x_a, y_a, 1, 1))

    def FrameGen(self, FramePack, Middlex, Middley, Cosangle, Sinangle, fork_send): #this function is only called on forks, no self.variables are modified
        if self.coloron == self.color_active:
            FRAME_PACK_SIZE = len(FramePack)
            frame = np.zeros(shape=(1024, 1024))
            framepack = [None]*FRAME_PACK_SIZE
            for k in range(FRAME_PACK_SIZE):
                for i in range(64):
                    LineData = FramePack[k][i]
                    midx = Middlex[k][i]
                    midy = Middley[k][i]
                    radcos = Cosangle[k][i]
                    radsin = Sinangle[k][i]

                    for j in range(512):
                        x = midx+radcos*j
                        y = midy+radsin*j
                        frame[round(x), round(y)] = LineData[j]
                framepack[k] = frame
            X, Y = SecurityZone().err_computing(framepack, self.range, self.security_radius)
        else:
            X = []
            Y = []
        fork_send.send((X, Y))

    def DrawCircles(self):
        GREEN = (64, 255, 64)
        BLUE = (64, 64, 255)
        if self.bold is False:
            pygame.draw.circle(self.window, GREEN, (512, 512), 512, 1)
            pygame.draw.circle(self.window, GREEN, (512, 512), 256, 1)
            pygame.draw.circle(self.window, GREEN, (512, 512), 128, 1)
            if self.displayradius is True and self.radius <= self.range and self.text != '':
                pygame.draw.circle(self.window, BLUE, (512, 512), int(self.radius*512/self.range), 1)

            font_scale = pygame.font.Font(None, 32)

            self.window.blit(font_scale.render(str(round(self.range/4))+'m', True, pygame.Color('dodgerblue2')), (516 - sqrt(15)/4*128, 128/4 + 508))
            self.window.blit(font_scale.render(str(round(self.range/2))+'m', True, pygame.Color('dodgerblue2')), (516 - sqrt(15)/4*256, 256/4 + 508))
            self.window.blit(font_scale.render(str(self.range)+'m', True, pygame.Color('dodgerblue2')), (516 - sqrt(15)/4*512, 512/4 + 508))

        else:
            pygame.draw.circle(self.window, GREEN, (512, 512), 512, 4)
            pygame.draw.circle(self.window, GREEN, (512, 512), 256, 4)
            pygame.draw.circle(self.window, GREEN, (512, 512), 128, 4)
            if self.displayradius is True and self.radius <= self.range and self.text != '':
                pygame.draw.circle(self.window, BLUE, (512, 512), int(self.radius*512/self.range), 4)

            font_scale = pygame.font.Font(None, 64)

            self.window.blit(font_scale.render(str(round(self.range / 4)) + 'm', True, pygame.Color('dodgerblue2')), (516 - sqrt(15)/4*128, 128/4 + 508))
            self.window.blit(font_scale.render(str(round(self.range / 2)) + 'm', True, pygame.Color('dodgerblue2')), (516 - sqrt(15)/4*256, 256/4 + 508))
            self.window.blit(font_scale.render(str(self.range) + 'm', True, pygame.Color('dodgerblue2')), (516 - sqrt(15)/4*512, 512/4 + 508))


    def MouseDistance(self, mouse_x, mouse_y):
        dist = sqrt((mouse_x-512)**2 + (mouse_y-512)**2)*self.range/512

        if dist <= self.range:
            if self.bold is True:
                font_mouse = pygame.font.Font(None, 48)
                self.window.blit(font_mouse.render(str(round(dist*100)/100)+'m', True, pygame.Color('brown1')), (mouse_x+10, mouse_y-6))
            else:
                font_mouse = pygame.font.Font(None, 24)
                self.window.blit(font_mouse.render(str(round(dist * 100) / 100) + 'm', True, pygame.Color('brown1')),
                                 (mouse_x + 10, mouse_y - 6))

    def DrawRectText(self):
        self.range_box.w = max(64, self.text_surf.get_width()+2)
        pygame.draw.rect(self.window, self.colortextrange, self.range_box, 2)

    ###########################################
    def DrawRectSecu(self):
        self.sec_rad_box.w = max(64, self.text_surf_rad.get_width() + 2)
        pygame.draw.rect(self.window, self.colorsecrad, self.sec_rad_box, 2)
        pygame.draw.rect(self.window, self.coloron, self.on_rect, 2)
        pygame.draw.rect(self.window, self.coloroff, self.off_rect, 2)

    def TextSurfSecu(self):
        self.text_surf_rad = self.font4.render(self.rad_text, True, self.colorsecrad)

        self.window.blit(self.font2.render('ON', True, self.coloron), (self.on_rect.x+3, self.on_rect.y+3))
        self.window.blit(self.font2.render('OFF', True, self.coloroff), (self.off_rect.x+3, self.off_rect.y+3))
        self.window.blit(self.text_surf_rad, (self.sec_rad_box.x+2, self.sec_rad_box.y+2))
    ###########################################

    def TextSurf(self):
        self.text_surf = self.font.render(self.text, True, self.colortextrange)
        self.window.blit(self.text_surf, (self.range_box.x+2, self.range_box.y+2))

    def DrawRectMenu(self):
        for i in range(16):
            pygame.draw.rect(self.window, self.color[i], self.rangemenu[i], 2)
        self.window.blit(self.font2.render('press the arrows', True, pygame.Color('dodgerblue2')), (10, 172))
        self.window.blit(self.font2.render('to navigate', True, pygame.Color('dodgerblue2')), (24, 188))


    def MenuSurf(self):
        for i in range(16):
            self.window.blit(self.font2.render(self.distance[i] + 'm', True, self.color[i]),
                             (self.rangemenu[i].x + 4, self.rangemenu[i].y + 4))

    def SpeedSurf(self):
        self.window.blit(self.font3.render(self.speed, True, pygame.Color('lightskyblue3')), (864, 8))
        self.window.blit(self.font2.render('press s for slow', True, pygame.Color('dodgerblue2')), (864, 32))
        self.window.blit(self.font2.render('press q for quick', True, pygame.Color('dodgerblue2')), (864, 44))
        self.window.blit(self.font2.render('press x for bolting', True, pygame.Color('dodgerblue2')), (864, 56))


    def DragDistance(self, bool, x, y):
        if bool is True:
            self.x_init = x
            self.y_init = y
        else:
            if sqrt((self.x_init-512)**2 + (self.y_init-512)**2) <= 512:
                if sqrt((x - 512) ** 2 + (y - 512) ** 2) <= 512:
                    self.xf = x
                    self.yf = y
                    pygame.draw.line(self.window, pygame.Color('brown1'), (self.x_init, self.y_init), (x, y), 2)
                    font_dist = pygame.font.Font(None, 24)
                    dist = sqrt((x-self.x_init)**2+(y-self.y_init)**2)*self.range/512
                    self.window.blit(font_dist.render('distance = ' + str(round(dist*100)/100) + 'm', True, pygame.Color('brown1')), (136, 8))
                else:
                    pygame.draw.line(self.window, pygame.Color('brown1'), (self.x_init, self.y_init), (self.xf, self.yf), 2)
                    font_dist = pygame.font.Font(None, 24)
                    dist = sqrt((self.xf - self.x_init) ** 2 + (self.yf - self.y_init) ** 2) * self.range / 512
                    self.window.blit(font_dist.render('Distance = ' + str(round(dist * 100) / 100) + 'm', True,
                                                      pygame.Color('brown1')), (136, 8))

    def DisplaySecRad(self):
        if self.coloron == self.color_active:
            font_rad = pygame.font.Font(None, 24)
            self.window.blit(font_rad.render('Zone = ' + str(self.security_radius) + 'm', True, pygame.Color('brown1')), (136, 28))

    def Window(self):
        return self.window

    def Surface(self):
        return self.surf

    def ChangeBold(self, key):
        if key == 2:  # 2 == KEYDOWN
            self.bold = True
        else:  # 3 == KEYUP
            self.bold = False
