from devices import *
import RPi.GPIO as GPIO
import time


#button = InputDevice(12,GPIO.PUD_UP)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12,GPIO.IN,GPIO.PUD_DOWN)

for i in range(100):
	print GPIO.input(12)
	time.sleep(.1)

