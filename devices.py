import RPi.GPIO as GPIO
import math
import time
import Adafruit_DHT
i = {}
o = {}

def setup():
	GPIO.setmode(GPIO.BOARD)

def is_in(device_name):
	return device_name in i

def is_out(device_name):
	return device_name in o

def get_in(device_name):
	if device_name not in i:
		error("input device {} doesn't exist".format(device_name))
	return i[device_name]

def get_out(device_name):
	if device_name not in o:
		error("output device {} doesn't exist".format(device_name))
	return o[device_name]

def set_in(device_name, device):
	global i
	if device_name in i:
		error('input device {} already declared'.format(device_name))
	if not isinstance(device, InputDevice):
		error('{} not InputDevice'.format(device))
	i[device_name] = device

def set_out(device_name, device):
	global o
	if device_name in o:
		error('output device {} already declared'.format(device_name))
	if not isinstance(device, OutputDevice):
		error('{} not OutputDevice'.format(device))
	o[device_name] = device

def cleanup():
	global o
	global i
	for _,device in o.iteritems():
		device.stop()
	o = {}
	i = {}
	GPIO.cleanup()

def error(msg):
	raise Exception('Runtime Device Error: {}'.format(msg))

class InputDevice:
	def __init__(self, channel, pull_up_down):
		self.channel = channel
		self.pull_up_down = pull_up_down
		GPIO.setup(channel, GPIO.IN, pull_up_down=pull_up_down)
	def input(self):
		return GPIO.input(self.channel)
	def wait_for_edge(self, type):
		return GPIO.wait_for_edge(self.channel, type)
	def __repr__(self):
		return "Input Device Channel # {}".format(self.channel)

class OutputDevice:
	def __init__(self, channel, freq):
		self.channel = channel
		GPIO.setup(channel, GPIO.OUT)
		self.freq = freq
		self.p = GPIO.PWM(channel, freq)
		self.started = False
	def start(self, dc):
		if dc < 0.0 or dc > 100.0:
			raise Exception('Bad dc {}'.format(dc))
		if self.started:
			raise Exception('Already started')
		self.p.start(dc)
		self.started = True
	def change_frequency(self, freq):
		if not self.started:
			raise Exception('Not started')
		self.p.ChangeFrequency(freq)
		self.freq = freq
	def change_duty_cycle(self, dc):
		if dc < 0.0 or dc > 100.0:
			raise Exception('Bad dc {}'.format(dc))
		if not self.started:
			raise Exception('Not started')
		self.p.ChangeDutyCycle(dc)
		self.dc = dc
	def stop(self):
		if not self.started:
			raise Exception('Not started')
		self.p.ChangeDutyCycle(0)
		self.p.stop()
		self.started = False
	def __repr__(self):
		return "Output Device Channel # {}".format(self.channel)


class FakeInput(InputDevice):
	def __init__(self, channel, pull_up_down):
		InputDevice.__init__(self, channel, pull_up_down)
		self.count = 0
	def get(self):
		self.count += 1
		return self.count

class TemperatureHumiditySensor(InputDevice):
	def __init__(self, channel):
		if channel is not 7:
			raise Exception('Temperature Sensor must be on gpio pin 7, pwm 4')
		#InputDevice.__init__(self,4,GPIO.PUD_DOWN)
		self.channel = 4
		self.LastTemp = None
		self.LastHumidity = None
	def getTemp(self):
		if self.LastTemp is None:
			humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, self.channel)
			if humidity is not None and temperature is not None:
				#print 'Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity)
				self.LastTemp = temperature
				self.LastHumidity = humidity
			else:
				print 'Failed to get reading. Try again!'
		return self.LastTemp
	def getHumidity(self):	
		if self.LastHumidity is None:
			humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
			if humidity is not None and temperature is not None:
				#print 'Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity)
				self.LastTemp = temperature
				self.LastHumidity = humidity
			else:
				print 'Failed to get reading. Try again!'
		return self.LastHumidity

class Led(OutputDevice):
	def __init__(self, channel, freq):
		OutputDevice.__init__(self, channel, freq)
		self.dc = 0
		self.start(self.dc)
	def set(self, on):
		self.dc = 100 if on else 0
		self.change_duty_cycle(self.dc)
	def get(self):
		return True if self.dc == 100 else 0
	def stop(self):
		self.change_duty_cycle(0)
		OutputDevice.stop(self)

class LightSensor(InputDevice):
	def __init__(self, channel, pull_up_down):
		InputDevice.__init__(self, channel, pull_up_down)
	def wait_for_press(self):
		if self.pull_up_down == GPIO.PUD_UP:
			self.wait_for_edge(GPIO.FALLING)
		else:
			self.wait_for_edge(GPIO.RISING)

class Button(InputDevice):
	def __init__(self, channel, pull_up_down):
		InputDevice.__init__(self, channel, pull_up_down)
	def wait_for_press(self):
		if self.pull_up_down == GPIO.PUD_UP:
			self.wait_for_edge(GPIO.FALLING)
		else:
			self.wait_for_edge(GPIO.RISING)
class Servo(OutputDevice):
	def __init__(self, channel):
		OutputDevice.__init__(self, channel, 50)
		self.dc = 0
		self.angle = 0
		self.start(self.dc)
	def degrees_to_DC(self, degrees):
		#num = 7.5-(5*math.sin(math.radians(degrees)))
		num = 7.5-5.0*(float(degrees)/90.0)
		return num
	def set_angle(self, degrees):
		if degrees < -90 or degrees > 90:
			raise Exception('Angle {} must be between -90 and 90'.format(degrees))
		self.angle = degrees
		self.change_duty_cycle(self.degrees_to_DC(degrees))
		time.sleep(1)
	def step_angle(self, increment):
		if self.angle + increment < -90 or self.angle + increment > 90:
			raise Exception('Increment {} makes angle {}, which must be between -90 and 90'.format(increment,self.angle+increment))
		self.angle = self.angle + increment
		self.change_duty_cycle(self.degrees_to_DC(self.angle))
		time.sleep(0.5)

class RgbLed(OutputDevice):
	def __init__(self, r_channel, g_channel, b_channel, freq):
		OutputDevice.__init__(self, r_channel, freq)
		self.b = OutputDevice(b_channel, freq)
		self.g = OutputDevice(g_channel, freq)
		self.start(0)
		self.g.start(0)
		self.b.start(0)
	def set_rgb(self, r, g, b):
		if r < 0.0 or r > 255.0 or g < 0.0 or g > 255.0 or b < 0.0 or b > 255.0:
			raise Exception('Invalid colors r: {} g: {} b: {}'.format(r, g, b))
		def normalize(val):
			return (val / 255.0) * 100
		self.change_duty_cycle(normalize(r))
		self.g.change_duty_cycle(normalize(g))
		self.b.change_duty_cycle(normalize(b))
	def stop(self):
		self.g.stop()
		self.b.stop()
		OutputDevice.stop(self)

