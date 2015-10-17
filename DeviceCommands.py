import devices

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
		return 'Wait Button {} Press'.format(self.device_name)

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

def translate_led_set(node):
	if 'Value' not in node or 'Device' not in node:
		translate_error('Malformed led set {}', node)
	return LedSet(node['Device'], translate_expression(node['Value']))

def translate_wait_button_press(node):
	if 'Device' not in node:
		translate_error('Malformed wait button press {}', node)
	return WaitButtonPress(node['Device'])

def translate_fake_get(node):
	if 'Device' not in node:
		translate_error('Malformed fake get {}', node)
	return FakeGet(node['Device'])

ExportedDeviceCommands = {'LedSet': translate_led_set, 'WaitButtonPress': translate_wait_button_press, 'FakeGet': translate_fake_get}
