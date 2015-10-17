import devices
import interpreter

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

class SetServoAngle:
	def __init__(self, device_name, val):
		self.device_name = device_name
		self.val = val
	def interp(self):
		print "Servo angle set"
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
		servo.set_angle(self.val.interp())
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

def translate_current_temp(node):
	if 'Device' not in node:
		translate_error('Malformed current temperature {}',node)
	return CurrentTemperature(node['Device'])

def translate_current_humidity(node):
	if 'Device' not in node:
		translate_error('Malformed current humidity {}',node)
	return CurrentHumidity(node['Device'])

def translate_led_set(node):
	if 'Value' not in node or 'Device' not in node:
		translate_error('Malformed led set {}', node)
	return LedSet(node['Device'], interpreter.translate_expression(node['Value']))

def translate_wait_button_press(node):
	if 'Device' not in node:
		translate_error('Malformed wait button press {}', node)
	return WaitButtonPress(node['Device'])
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

ExportedDeviceCommands = {'LedSet': translate_led_set, 'WaitButtonPress': translate_wait_button_press, 'FakeGet': translate_fake_get, 'SetServoAngle': translate_set_servo_angle, 'StepServoAngle': translate_step_servo_angle, 'CurrentTemperature': translate_current_temp, 'CurrentHumidity':translate_current_humidity}
