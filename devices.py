import RPi.GPIO as GPIO

i = {}
o = {}

def setup():
	GPIO.setmode(GPIO.BOARD)

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
	for _,device in o.iteritems():
		device.stop()
	GPIO.cleanup()

def error(msg):
	raise Exception('Runtime Device Error: {}', msg)

class InputDevice:
	def __init__(self, channel, pull_up_down):
		self.channel = channel
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
		self.p = GPIO.PWM(channel, freq)
		self.started = False
		self.stopped = False
	def start(self, dc):
		if dc < 0.0 or dc > 100.0:
			raise Exception('Bad dc {}'.format(dc))
		if self.stopped:
			raise Exception('Already stopped')
		if self.started:
			raise Exception('Already started')
		self.p.start(dc)
		self.started = True
	def change_frequency(self, freq):
		if not self.started:
			raise Exception('Not started')
		if self.stopped:
			raise Exception('Already stopped')
		self.p.ChangeFrequency(freq)
	def change_duty_cycle(self, dc):
		if not self.started:
			raise Exception('Not started')
		if self.stopped:
			raise Exception('Already stopped')
		self.p.ChangeDutyCycle(dc)
	def stop(self):
		if not self.started:
			raise Exception('Not started')
		if self.stopped:
			raise Exception('Already stopped')
		self.p.stop()
		self.started = False
		self.stopped = True
	def __repr__(self):
		return "Output Device Channel # {}".format(self.channel)

class Led(OutputDevice):
	def __init__(self, channel, on):
		OutputDevice.__init__(self, channel, 1.0)
		self.dc = 100 if on else 0
		self.start(self.dc)
	def set(self, on):
		self.dc = 100 if on else 0
		self.change_duty_cycle(self.dc)
	def get(self):
		return True if self.dc == 100 else 0

class Button(InputDevice):
	def __init__(self, channel, pull_up_down):
		OutputDevice.__init__(self, channel, pull_up_down)
	def wait_for_press(self):
		if self.pull_up_down == GPIO.PUD_UP:
			self.wait_for_edge(GPIO.FALLING)
		else:
			self.wait_for_edge(GPIO.RISING)

