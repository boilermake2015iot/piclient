import RPi.GPIO as GPIO

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
	for _,device in o.iteritems():
		device.stop()
	GPIO.cleanup()

def error(msg):
	raise Exception('Runtime Device Error: {}', msg)

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

class Button(InputDevice):
	def __init__(self, channel, pull_up_down):
		InputDevice.__init__(self, channel, pull_up_down)
	def wait_for_press(self):
		if self.pull_up_down == GPIO.PUD_UP:
			self.wait_for_edge(GPIO.FALLING)
		else:
			self.wait_for_edge(GPIO.RISING)

