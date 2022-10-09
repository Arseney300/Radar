import RadarDecoder
import RadarListener
import RadarRender
import SecurityZone

from sys import exit
import numpy as np
import pygame
from pygame.locals import *
import os
from multiprocessing import Pipe, Process


#######################INITIALISATION#######################
lastredraw = 0
lastdrawnangle = 0
oldzoom = 0
oldangle = 0
FrameUpdater = 0
framecount = 0
default_range = 100

############################################################

###########SECURITY ZONE VARIABLE INITIALISATION############
FRAME_PACK_SIZE = 8  #number of frames in a pack
FRAME_DATA_FRAG = 64  #number of loops to make one single frame
LINE_A_LOOP = 32

X = []
Y = []
i = 0
fork_recv, fork_send = Pipe()


LineData32 = [None]*FRAME_DATA_FRAG*LINE_A_LOOP
MidyComp = [None]*FRAME_DATA_FRAG*LINE_A_LOOP
MidxComp = [None]*FRAME_DATA_FRAG*LINE_A_LOOP
RadcosComp = [None]*FRAME_DATA_FRAG*LINE_A_LOOP
RadsinComp = [None]*FRAME_DATA_FRAG*LINE_A_LOOP

FramePack = [None]*FRAME_PACK_SIZE
Cosangle = [None]*FRAME_PACK_SIZE
Sinangle = [None]*FRAME_PACK_SIZE
Middlex = [None]*FRAME_PACK_SIZE
Middley = [None]*FRAME_PACK_SIZE

framepack_count = 0
data_count = 0
############################################################

###################CALLING OF THE CLASSES###################
decod = RadarDecoder.RadarDecoder()
listen = RadarListener.RadarListener()
render = RadarRender.RadarRender()
image = SecurityZone.SecurityZone()
############################################################

#####################PRIMARY OBJECTS########################
listen.RadarTurnOn()
listen.Distance(default_range)
listen.TargetBoost()
listen.LocalInterferenceFilter()
listen.InterferenceRejection()
listen.Preprocessing()
render.InitSpeed('slow: 24rpm')
FrameHeader = np.zeros(8)
LineHeader = np.zeros(24)
LineData = np.empty(512)

window = render.Window()
surf = render.Surface()
############################################################

while listen.State() is True:
    k = 0
    packets = listen.RadarListen() # receiving the datas of one line
    FrameHeader = packets[:8]
    k += 8
    while len(packets) > k:
        LineHeader = packets[k:24+k]
        k += 24
        LineData = packets[k:512+k]
        k += 512
        angleraw, angle = decod.Cordinates(LineHeader)
        midx, radcos, midy, radsin, lastdrawnangle, oldangle = decod.RenderCordinates(angleraw, angle, framecount, lastdrawnangle, oldangle)

        ################RENDERING THE FRAMES####################

        if 0 < len(X): #32 pixels can be displayed
            if i < len(X):
                render.Frame(LineData, midx, radcos, midy, radsin, X[i], Y[i]) #something is moving, displaying red pixels
                i += 1
            else:
                i = 0 #we reloop the red pixels display
                render.Frame(LineData, midx, radcos, midy, radsin, X[i], Y[i])
        else:
            render.Frame(LineData, midx, radcos, midy, radsin, 512, 512)


    #displays a red pixel in the middle of the screen: everything in order

        #########################################################
        ##############BUILDING OF A SINGLE FRAME#################
        LineData32[int((k-8)/(len(packets)-8)*LINE_A_LOOP)-1+data_count*LINE_A_LOOP] = LineData
        MidxComp[int((k-8)/(len(packets)-8)*LINE_A_LOOP)-1+data_count*LINE_A_LOOP] = midx
        MidyComp[int((k-8)/(len(packets)-8)*LINE_A_LOOP)-1+data_count*LINE_A_LOOP] = midy
        RadcosComp[int((k-8)/(len(packets)-8)*LINE_A_LOOP)-1+data_count*LINE_A_LOOP] = radcos
        RadsinComp[int((k-8)/(len(packets)-8)*LINE_A_LOOP)-1+data_count*LINE_A_LOOP] = radsin
        #########################################################
    data_count += 1
    ###############BUILDING OF A FRAME PACK##################
    if framepack_count < FRAME_PACK_SIZE:
        if data_count == FRAME_DATA_FRAG:
            data_count = 0
            FramePack[framepack_count] = LineData32 #single frame
            Middlex[framepack_count] = MidxComp
            Middley[framepack_count] = MidyComp
            Sinangle[framepack_count] = RadsinComp
            Cosangle[framepack_count] = RadcosComp

            print(framepack_count)
            framepack_count += 1
    #########################################################

    ################FORKING THE FRAME PACK###################
    else:
        data_count = 0
        framepack_count = 0
        # print(np.asarray(FramePack[3]))

        fork = Process(target=render.FrameGen, args=(FramePack, Middlex, Middley, Cosangle, Sinangle, fork_send))
        fork.start()
        (X, Y) = fork_recv.recv()

    #########################################################

    #######################DISPLAY###########################

    window.blit(surf, (0, 0))

    render.TextSurf()
    render.TextSurfSecu()
    render.MenuSurf()
    render.SpeedSurf()

    render.DrawCircles()
    render.DrawRectText()
    render.DrawRectSecu()
    render.DrawRectMenu()
    render.DisplaySecRad()

    mouse_x, mouse_y = pygame.mouse.get_pos()
    render.MouseDistance(mouse_x, mouse_y)

    if pygame.mouse.get_pressed()[0]:
        render.DragDistance(False, mouse_x, mouse_y)

    pygame.display.update() #flip()
    ##################EVENTS GESTION########################
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            listen.RadarTurnOff()
            pygame.quit()
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_UP or K_DOWN: #up and down arrows
                render.ScaleRange(event.key)
            if event.key == K_s or event.key == K_q or event.key == K_x:
                render.ChangeSpeed(event.key)
            if event.key == K_SPACE:
                render.ChangeBold(event.type)
            else:
                render.TextRangeCircle(event)
                render.TextSecuRadius(event)
        elif event.type == KEYUP:
            if event.key == K_SPACE:
                render.ChangeBold(event.type)
        elif event.type == MOUSEBUTTONDOWN:
            render.DragDistance(True, mouse_x, mouse_y)
            render.ColorAct(event)
    listen.KeepAlive()
