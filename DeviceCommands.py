import devices
import interpreter
import time

class LedSet:
	def __init__(self, device_name, val):
		self.device_name = device_name
		self.val = val
	def interp(self):
		led = devices.get_out(self.device_name)
		if not isinstance(led, devices.Led):
			devices.error('device {} is the wrong type'.format(led))
		led.set(self.val.interp())
	def __repr__(self):
		return "Led {} Set {}".format(self.device_name, self.val.__repr__())

class LedBlink:
	def __init__(self, device_name, blink_interval, number_of_blinks):
		self.device_name = device_name
		self.blink_interval = blink_interval
		self.number_of_blinks = number_of_blinks
	def interp(self):
		led = devices.get_out(self.device_name)
		if not isinstance(led, devices.Led):
			devices.error('device {} is the wrong type'.format(led))
		dc = led.dc
		freq = led.freq
		#led.change_frequency(0.5)
		led.change_frequency(1.0 / self.blink_interval.interp())
		led.change_duty_cycle(50)
		time.sleep(self.blink_interval.interp() * self.number_of_blinks.interp())
		led.change_duty_cycle(dc)
		led.change_frequency(freq)
		"""
		for i in range(0,self.number_of_blinks.interp()):
			led.set(1)
			time.sleep(0.25)
			led.set(0)
			time.sleep(self.blink_interval.interp())
		"""
	def __repr__(self):
		return "Led {} Blink".format(self.device_name)

class GetButtonStatus:
	def __init__(self, device_name):
		self.device_name = device_name
	def interp(self):
		button = devices.get_in(self.device_name)
		if not isinstance(button, devices.Button):
			devices.error('device {} is the wrong type'.format(button))
		return button.input()
	def __repr__(self):
		return 'Get value of button {}'.format(self.device_name)

class WaitButtonPress:
	def __init__(self, device_name):
		self.device_name = device_name
	def interp(self):
		button = devices.get_in(self.device_name)
		if not isinstance(button, devices.Button):
			devices.error('device {} is the wrong type'.format(button))
		button.wait_for_press()
	def __repr__(self):
		return 'Wait On Button {} Press'.format(self.device_name)

class GetLightStatus:
	def __init__(self, device_name):
		self.device_name = device_name
	def interp(self):
		light = devices.get_in(self.device_name)
		if not isinstance(light, devices.LightSensor):
			devices.error('device {} is the wrong type'.format(light))
		return light.input()
	def __repr__(self):
		return 'Get value of button {}'.format(self.device_name)

class WaitLightLow:
	def __init__(self, device_name):
		self.device_name = device_name
	def interp(self):
		light = devices.get_in(self.device_name)
		if not isinstance(light, devices.LightSensor):
			devices.error('device {} is the wrong type'.format(button))
		light.wait_for_press()
	def __repr__(self):
		return 'Wait On Button {} Press'.format(self.device_name)

class SetServoAngle:
	def __init__(self, device_name, val):
		self.device_name = device_name
		self.val = val
	def interp(self):
		servo = devices.get_out(self.device_name)
		if not isinstance(servo, devices.Servo):
			devices.error('Device {} is the wrong type'.format(servo))
		servo.set_angle(self.val.interp())
	def __repr__(self):
		return 'Servo {}\'s Angle set {}'.format(self.device_name,self.val.__repr__())

class StepServoAngle:
	def __init__(self, device_name, val):
		self.device_name = device_name
		self.val = val
	def interp(self):
		servo = devices.get_out(self.device_name)
		if not isinstance(servo, devices.Servo):
			devices.error('Device {} is the wrong type'.format(servo))
		servo.step_angle(self.val.interp())
	def __repr__(self):
		return 'Servo {}\'s Angle stepped {}'.format(self.device_name,self.val.__repr__())



class FakeGet:
	def __init__(self, device_name):
		self.device_name = device_name
	def interp(self):
		fake = devices.get_in(self.device_name)
		if not isinstance(fake, devices.FakeInput):
			devices.error('device {} is the wrong type'.format(fake))
		return fake.get()
	def __repr__(self):
		return 'Fake {} Get'.format(self.device_name)

class CurrentTemperature:
	def __init__(self, device_name):
		self.device_name = device_name
	def interp(self):
		sensor = devices.get_in(self.device_name)
		if not isinstance(sensor, devices.TemperatureHumiditySensor):
			devices.error('device {} is the wrong type'.format(sensor))
		print sensor.getTemp()
		return sensor.getTemp()
	def __repr__(self):
		return 'Current Temperature using sensor {}'.format(self.device_name)

class CurrentHumidity:
	def __init__(self, device_name):
		self.device_name = device_name
	def interp(self):
		sensor = devices.get_in(self.device_name)
		if not isinstance(sensor, devices.TemperatureHumiditySensor):
			devices.error('device {} is the wrong type'.format(sensor))
		return sensor.getHumidity()
	def __repr__(self):
		return 'Current Humidity using sensor {}'.format(self.device_name)

class SetRgbLed:
	def __init__(self, device_name, r, g, b):
		self.device_name = device_name
		self.r = r
		self.g = g
		self.b = b
	def interp(self):
		rgb_led = devices.get_out(self.device_name)
		if not isinstance(rgb_led, devices.RgbLed):
			devices.error('device {} is the wrong type'.format(self.device_name))
		rgb_led.set_rgb(self.r.interp(), self.g.interp(), self.b.interp())
	def __repr__(self):
		return 'SetRgbLed {}'.format(self.device_name)

def translate_current_temp(node):
	if 'Device' not in node:
		translate_error('Malformed current temperature {}',node)
	return CurrentTemperature(node['Device'])

def translate_current_humidity(node):
	if 'Device' not in node:
		translate_error('Malformed current humidity {}',node)
	return CurrentHumidity(node['Device'])

def translate_led_blink(node):
	if 'BlinkInterval' not in node or 'NumberOfBlinks' not in node or 'Device' not in node:
		translate_error('Malformed led blink {}', node)
	return LedBlink(node['Device'], interpreter.translate_expression(node['BlinkInterval']),interpreter.translate_expression(node['NumberOfBlinks']))

def translate_led_set(node):
	if 'Value' not in node or 'Device' not in node:
		translate_error('Malformed led set {}', node)
	return LedSet(node['Device'], interpreter.translate_expression(node['Value']))

def translate_get_button(node):
	if 'Device' not in node:
		translate_error('Malformed get button status {}', node)
	return GetButtonStatus(node['Device'])

def translate_wait_button_press(node):
	if 'Device' not in node:
		translate_error('Malformed wait button press {}', node)
	return WaitButtonPress(node['Device'])

def translate_get_light(node):
	if 'Device' not in node:
		translate_error('Malformed get light status {}', node)
	return GetLightStatus(node['Device'])

def translate_wait_light(node):
	if 'Device' not in node:
		translate_error('Malformed wait light press {}', node)
	return WaitLightHigh(node['Device'])

def translate_set_servo_angle(node):
	if 'Angle' not in node or 'Device' not in node:
		translate_error('Malformed set servo angle {}', node)
	return SetServoAngle(node['Device'], interpreter.translate_expression(node['Angle']))

def translate_step_servo_angle(node):
	if 'Increment' not in node or 'Device' not in node:
		translate_error('Malformed step servo angle {}', node)
	return StepServoAngle(node['Device'], interpreter.translate_expression(node['Increment']))

def translate_fake_get(node):
	if 'Device' not in node:
		translate_error('Malformed fake get {}', node)
	return FakeGet(node['Device'])

def translate_set_rgb_led(node):
	if 'Device' not in node or 'R' not in node or 'G' not in node or 'B' not in node:
		translate_error('MAlformed set rgb led {}', node)
	return SetRgbLed(node['Device'], interpreter.translate_expression(node['R']), interpreter.translate_expression(node['G']), interpreter.translate_expression(node['B']))

ExportedDeviceCommands = {'LedSet': translate_led_set, 'WaitButtonPress': translate_wait_button_press, 'FakeGet': translate_fake_get, 'SetServoAngle': translate_set_servo_angle, 'StepServoAngle': translate_step_servo_angle, 'CurrentTemperature': translate_current_temp, 'CurrentHumidity':translate_current_humidity, 'GetButtonStatus': translate_get_button, 'GetLightStatus': translate_get_light, 'WaitLightHigh': translate_wait_light, 'SetRgbLed': translate_set_rgb_led, 'LedBlink': translate_led_blink}
