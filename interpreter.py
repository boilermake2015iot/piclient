import json, time, devices

class If:
	def __init__(self, cond, page_name):
		self.cond = cond
		self.page_name = page_name
	def interp(self):
		if self.page_name not in page_decls:
			raise Exception('Runtime Error: page {} not declared'.format(page_name))
		if (self.cond.interp()):
			page_decls[self.page_name].interp()
	def __repr__(self):
		return "if {}: {} else: {}".format(self.cond.__repr__(), self.true_node.__repr__(), self.cond.false_node.__repr__())

opToFn = {
	'+': lambda lhs, rhs: lhs + rhs,
	'-': lambda lhs, rhs: lhs - rhs,
	'/': lambda lhs, rhs: lhs / rhs,
	'*': lambda lhs, rhs: lhs * rhs,
	'>': lambda lhs, rhs: lhs > rhs,
	'<': lambda lhs, rhs: lhs < rhs,
	'>=': lambda lhs, rhs: lhs >= rhs,
	'<=': lambda lhs, rhs: lhs <= rhs,
	'=': lambda lhs, rhs: lhs == rhs,
	'!=': lambda lhs, rhs: lhs != rhs
}

class Expression:
	def __init__(self, op, lhs, rhs):
		if op not in opToFn:
			raise Exception("Unknown operator {}".format(op))
		self.op_str = op
		self.op = opToFn[op]
		self.lhs = lhs
		self.rhs = rhs
	def interp(self):
		return self.op(self.lhs.interp(), self.rhs.interp())
	def __repr__(self):
		return "{} {} {}".format(self.lhs.__repr__(), self.op_str, self.rhs.__repr__())

class Constant:
	def __init__(self, constant):
		self.constant = constant
	def interp(self):
		return self.constant
	def __repr__(self):
		return self.constant.__repr__()

class LedSet:
	def __init__(self, device_name, val):
		self.device_name = device_name
		self.val = val
	def interp(self):
		led = devices.get_in(self.device_name)
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

class Print:
	def __init__(self, param):
		self.param = param
	def interp(self):
		print self.param.interp()
	def __repr__(self):
		return "print({})".format(self.param.__repr__())

class PageDecl:
	def __init__(self, name, nodes):
		self.name = name
		self.nodes = nodes
	def interp(self):
		for node in self.nodes:
			node.interp()
	def __repr__(self):
		print self.nodes.__repr__()
		return "Name: {}, Nodes: {}".format(self.name, self.nodes.__repr__())

def translate_error(msg, node):
	raise Exception(msg.format(json.dumps(node)))

def translate_constant(node):
	if 'Value' not in node:
		translate_error('Malformed constant {}', node)
	return Constant(node['Value'])

def translate_expression(node):
	if node['Type']== 'Constant':
		return translate_constant(node)
	elif node['Type'] == 'Expression':
		if 'Op' not in node or 'Left' not in node or 'Right' not in node:
			translate_error('Malformed expression {}', node)
		return Expression(node['Op'], translate_expression(node['Left']), translate_expression(node['Right']))
	else:
		translate_error('Invalid expression node {}', node)

def translate_if(node):
	if 'Condition' not in node or 'Page' not in node:
		translate_error('Malformed page {}', node)
	return If(translate_expression(node['Condition']), node['Page'])

def translate_print(node):
	if 'Param' not in node:
		translate_error('Malformed print {}', node)
	return Print(translate_expression(node['Param']))

def translate_led_set(node):
	if 'Value' not in node or 'Device' not in node:
		translate_error('Malformed led set {}', node)
	return LedSet(node['Device'], translate_expression(node['Value']))

def translate_wait_button_press(node):
	if 'Device' not in node:
		translate_error('Malformed wait button press {}', node)
	return WaitButtonPress(node['Device'])

def translate_page_decl(page):
	if 'Name' not in page or 'Nodes' not in page:
		translate_error('Malformed page {}', page)
	return PageDecl(page['Name'], translate_nodes(page['Nodes']))
	
def translate_nodes(nodes):
	translated = []
	for node in nodes:
		if 'Type' not in node:
			translate_error('Malformed node {}', node)
		if node['Type'] == 'If':
			translated.append(translate_if(node))
		elif node['Type'] == 'Print':
			translated.append(translate_print(node))
		elif node['Type'] == 'LedSet':
			translated.append(translate_led_set(node))
		elif node['Type'] == 'WaitButtonPress':
			translated.append(translate_wait_button_press(node))
		else:
			translate_error('Malformed node {}', node)
	return translated

page_decls = {}

def interp(doc):
	global page_decls
	page_decls = {}
	if 'Pages' not in doc:
		raise Exception("Malformed doc {}".format(json.dumps(doc)))
	for page_doc in doc['Pages']:
		page_decl = translate_page_decl(page_doc)
		page_decls[page_decl.name] = page_decl
	if 'Main' not in page_decls:
		raise Exception('Malformed doc - no main {}'.format(json.dumps(doc)))
	page_decls['Main'].interp()

devices.setup()

devices.set_in('RedLed', devices.Led(7, 50))
devices.set_out('Button', devices.Button(8, GPIO.PUD_UP))

interp({'Pages': [{'Name': 'Main', 'Nodes': [{'Type': 'Print', 'Param': {'Type': 'Constant', 'Value': 5}}]}]})

interp({'Pages': [{'Name': 'Main', 'Nodes': [{'Type': 'If', 'Condition': {'Type': 'Expression', 'Op': '>', 'Left': {'Type': 'Constant', 'Value': 5}, 'Right': {'Type': 'Constant', 'Value': 4}}, 'Page': 'Sub'}, {'Type': 'Print', 'Param': {'Type': 'Constant', 'Value': 'OK2'}}]}, {'Name': 'Sub', 'Nodes': [{'Type': 'Print', 'Param': {'Type': 'Constant', 'Value': 'OK'}}]}]})

interp({'Pages': [{'Name': 'Main', 'Nodes': [{'Type': 'WaitButtonPress', 'Device': 'Button'}]}]})

interp({'Pages': [{'Name': 'Main', 'Nodes': [{'Type': 'LedSet', 'Device': 'RedLed', 'Value': {'Type': 'Constant', 'Value': True}}]}]})

time.sleep(1)

devices.cleanup()
