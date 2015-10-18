import RPi.GPIO as GPIO
import time
# board mode
GPIO.setmode(GPIO.BOARD)
"""
GPIO.setup(8, GPIO.OUT)
p = GPIO.PWM(8, 50)
p.start(50)
raw_input('Press return to stop:')
#p.stop()
#GPIO.output(8, GPIO.HIGH)
#time.sleep(10)
"""
GPIO.setup(13, GPIO.OUT)

GPIO.output(13, True)
time.sleep(2)

"""
p = GPIO.PWM(7, 50)
p.start(0)
try:
	while True:
		for dc in range(0, 101, 5):
			p.ChangeDutyCycle(dc)
			time.sleep(0.1)
		for dc in range(100, -1, -5):
			p.ChangeDutyCycle(dc)
			time.sleep(0.1)
except KeyboardInterrupt:
	pass
p.stop()
"""
GPIO.cleanup()
