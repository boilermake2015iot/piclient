import RPi.GPIO as GPIO
import time
# board mode
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)
GPIO.output(7, True)
time.sleep(10)
GPIO.cleanup()
