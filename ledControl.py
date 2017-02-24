from gpiozero import RGBLED
from time import sleep

led = RGBLED(13, 19, 26)

def updateLED(utilization):
	
	# Check for invalid input
	if utilization > 1:
		print("Warning: CPU utilization reported over 100%")
	elif utilization < 0:
		print("Warning: CPU utilization reported under 0%")
	
	if utilization <= .25:
		# green
		led.color = (0, 1, 0)
	elif utilization <= .5:
		# yellow
		led.color = (1, .5, 0)
	else:
		# red
		led.color = (1, 0, 0)
	
# Test code (remove before integrating)	
while(1):
	updateLED(.2)
	sleep(1)
	updateLED(.3)
	sleep(1)
	updateLED(.6)
	sleep(1)
