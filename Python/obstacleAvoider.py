#! /usr/bin/env python
#
# Obstacle avoider with Picon Zero

import piconzero as pz, hcsr04, time

#======================================================================
# Reading single character by forcing stdin to raw mode
import sys
import tty
import termios

def readchar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    if ch == '0x03':
        raise KeyboardInterrupt
    return ch

def readkey(getchar_fn=None):
    getchar = getchar_fn or readchar
    c1 = getchar()
    if ord(c1) != 0x1b:
        return c1
    c2 = getchar()
    if ord(c2) != 0x5b:
        return c1
    c3 = getchar()
    return chr(0x10 + ord(c3) - 65)  # 16=Up, 17=Down, 18=Right, 19=Left arrows

# End of single character reading
#======================================================================

def distance2Pixel(dist):
        pz.setAllPixels(0,0,0)
	if (dist > 80):
		dist = 80
	if (dist < 15):
		green = 0
		red = 255
		blue = 0
	elif (dist < 30):
		green = 165
		red = 255
		blue = 0
	else:
		green = 255
		red = 0
		blue = 0

        for i in range(8-dist/10):
		pz.setPixel(i,red,green,blue)

#	if (dist >= 80):
#		pz.setPixel(7,0,255,0)
#	if (dist >= 70):
#		pz.setPixel(6,0,255,0)
#	if (dist <= 60):
#		pz.setPixel(5,0,255,0)
#	if (dist <= 50):
#		pz.setPixel(4,0,255,0)
#	if (dist <= 40):
#		pz.setPixel(3,0,255,0)
#	if (dist <= 30):
#		pz.setPixel(2,0,255,0)
#	if (dist <= 20):
#		pz.setPixel(1,0,255,0);
#	else:
#		pz.setPixel(0,0,255,0);

speed = 60

print("Tests the motors by using the arrow keys to control")
print("Use , or < to slow down")
print("Use . or > to speed up")
print("Speed changes take effect when the next arrow key is pressed")
print("Press Ctrl-C to end")
print()

pz.init()
pz.setOutputConfig(5, 3)    # set output 5 to WS2812
rev = pz.getRevision()
print(rev[0], rev[1])
hcsr04.init()

try:
    distance = int(hcsr04.getDistance())
    while (distance > 10):
        distance = int(hcsr04.getDistance())
        pz.stop()
    while True:
        distance = int(hcsr04.getDistance())
        print "Distance:", distance
        distance2Pixel(distance) 
	if (distance <= 15):
		pz.stop()
		time.sleep(1)
		while (distance <= 25):
			distance = int(hcsr04.getDistance())
			pz.spinLeft(speed);
	else:
		pz.forward(speed)	

#        keyp = readkey()
#        if keyp == 'w' or ord(keyp) == 16:
#            pz.forward(speed)
#            print('Forward', speed)
#        elif keyp == 'z' or ord(keyp) == 17:
#            pz.reverse(speed)
#            print('Reverse', speed)
#        elif keyp == 's' or ord(keyp) == 18:
#            pz.spinRight(speed)
#            print('Spin Right', speed)
#        elif keyp == 'a' or ord(keyp) == 19:
#            pz.spinLeft(speed)
#            print('Spin Left', speed)
#        elif keyp == '.' or keyp == '>':
#            speed = min(100, speed+10)
#            print('Speed+', speed)
#        elif keyp == ',' or keyp == '<':
#            speed = max (0, speed-10)
#            print('Speed-', speed)
#        elif keyp == ' ':
#            pz.stop()
#            print('Stop')
#        elif ord(keyp) == 3:
#            break
	time.sleep(0.1)

except KeyboardInterrupt:
    print

except KeyboardInterrupt:
    print

finally:
    pz.cleanup()
    hcsr04.cleanup()

