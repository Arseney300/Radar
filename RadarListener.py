import socket
import struct
import numpy as np

class RadarListener(object):
    def __init__(self):
        self.MCAST_GRP = '236.6.7.8'
        self.MCAST_PORT = 6678

        self.HOST2 = '236.6.7.10'
        self.PORT2 = 6680

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('236.6.7.8', self.MCAST_PORT))  # use MCAST_GRP instead of '' to listen only
                             # to MCAST_GRP, not all groups on MCAST_PORT
        mreq = struct.pack("4sl", socket.inet_aton(self.MCAST_GRP), socket.INADDR_ANY)

        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        self.sock2 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.data = np.zeros(17160)
        self.RadarState = False

    def RadarTurnOn(self):
        start1=bytes([0x00, 0xC1, 0x01])
        start2=bytes([0x01, 0xC1, 0x01])
        self.sock2.sendto(start1, (self.HOST2, self.PORT2))
        self.sock2.sendto(start2, (self.HOST2, self.PORT2))
        self.RadarState = True

    def RadarTurnOff(self):
        finish1=bytes([0x00, 0xC1, 0x00])
        finish2=bytes([0x01, 0xC1, 0x00])
        self.sock2.sendto(finish1, (self.HOST2, self.PORT2))
        self.sock2.sendto(finish2, (self.HOST2, self.PORT2))
        self.sock2.close()
        self.sock.close()
        self.RadarState = False

    def Distance(self, r):
        distance = {50: bytes([0x03, 0xC1, 0xf4, 0x01, 0, 0]),
        75: bytes([0x03, 0xC1, 0xee, 0x02, 0, 0]),
        100: bytes([0x03, 0xC1, 0xee, 0x03, 0, 0]),
        250: bytes([0x03, 0xC1, 0xc4, 0x09, 0, 0]),
        500: bytes([0x03, 0xC1, 0x88, 0x13, 0, 0]),
        750: bytes([0x03, 0xC1, 0x4c, 0x1d, 0, 0]),
        1000: bytes([0x03, 0xC1, 0x10, 0x27, 0, 0]),
        1500: bytes([0x03, 0xC1, 0x80, 0xA9, 3, 0]),
        2000: bytes([0x03, 0xC1, 0x20, 0x4e, 0, 0]),
        3000: bytes([0x03, 0xC1, 0x30, 0x75, 0, 0]),
        4000: bytes([0x03, 0xC1, 0x40, 0x9c, 0, 0]),
        6000: bytes([0x03, 0xC1, 0x60, 0xea, 0, 0]),
        8000: bytes([0x03, 0xC1, 0x80, 0x38, 1, 0]),
        12000: bytes([0x03, 0xC1, 0xc0, 0xd4, 1, 0]),
        16000: bytes([0x03, 0xC1, 0x00, 0x71, 2, 0]),
        24000: bytes([0x03, 0xC1, 0x80, 0xa9, 3, 0])}
        if r in distance:
            self.sock2.sendto(distance[r], (self.HOST2, self.PORT2))

    def Preprocessing(self):
        self.sock2.sendto(bytes([0x06, 0xC1, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF]), (self.HOST2, self.PORT2))

    def LocalInterferenceFilter(self):
        self.sock2.sendto(bytes([0x0E, 0xC1, 0x03]), (self.HOST2, self.PORT2))


    def ScanSpeed(self, s):
        speed = {'slow': bytes([0x0F, 0xC1, 0x00]), 'quick': bytes([0x0F, 0xC1, 0x01]), 'bolting': bytes([0x0F, 0xC1, 0x02])}
        if s in speed:
            self.sock2.sendto(speed[s], (self.HOST2, self.PORT2))

    def KeepAlive(self):
        self.sock2.sendto(bytes([0xA0, 0xC1, 0]), (self.HOST2, self.PORT2))

    def TargetBoost(self):
        self.sock2.sendto(bytes([0x0A, 0xC1, 0]), (self.HOST2, self.PORT2))

    def InterferenceRejection(self):
        self.sock2.sendto(bytes([0x08, 0xC1, 0x00]), (self.HOST2, self.PORT2))

    def TotalReboot(self):
        self.sock2.sendto(bytes([0x00, 0xC1, 0x00]), ((self.HOST2, self.PORT2)))

    def State(self):
        return self.RadarState

    def RadarListen(self):
        while self.RadarState is True:
            self.data = self.sock.recv(65536)
            return self.data
