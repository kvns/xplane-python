"""
    XplaneControl.py
    
    Example of controlling X-Plane from a python script over 
    UDP network communication.

    Author: Kevin Smith (kvns@sixdof.net)
"""

import socket
import time
import struct
import math

# the host this is running on.
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
sock.bind(("0.0.0.0", 49001))

# the host this is connecting to (where X-Plane is running)
outsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
outsock.connect(("127.0.0.1",49000))

yokestr = "sim/joystick/yoke_roll_ratio"
sfill = yokestr + ((500 - len(yokestr)) * '\0')

ovyoke = "sim/operation/override/override_joystick"
ovyoke = ovyoke + ((500 - len(ovyoke)) * '\0')

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    num = 0
    unp = []
    thetime = 0.0
    if data[0:4] == "DATA":
        nummsg = (len(data)-5)/38
        for n in xrange(nummsg):
            p = struct.unpack('iffffffff',data[(5+n*36):(5+n*36+36)])
            if p[0] == 1:
                thetime = p[1]
                
    pitchval = 1.0 * math.cos( 2*math.pi / 3.0 * thetime )
    pitchmsg = "DREF0" + struct.pack("f",pitchval) + sfill
    overmsg = "DREF0" + struct.pack("i",1) + ovyoke
    outsock.sendall(overmsg)
    outsock.sendall(pitchmsg)
    print thetime,pitchval
