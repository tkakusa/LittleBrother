from gpiozero import LED
from time import sleep

red = LED(13)
green = LED(19)
blue = LED(26)

def updateLED(utilization):
	if utilization <= .25:
		red.off()
		green.on()
		blue.off()
	elif utilization <= .5:
		red.on()
		green.on()
		blue.off()
	else:
		red.on()
		green.off()
		blue.off()
		
while(1):
	updateLED(.2)
	sleep(1)
	updateLED(.3)
	sleep(1)
	updateLED(.6)
	sleep(1)
