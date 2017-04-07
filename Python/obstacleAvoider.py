#! /usr/bin/env python
#
# Obstacle avoider with Picon Zero

import piconzero as pz, hcsr04, time

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

def main():

	speed = 60

	print("Simple obstacle avoider")	
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

		time.sleep(0.1)

	finally:
	    pz.cleanup()
	    hcsr04.cleanup()

if __name__== "__main__":
	main()


