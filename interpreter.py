import json

class Device:
	def __init__(self, channel):
		self.channel = channel

class If:
	def __init__(self, cond, true_block, false_block):
		self.cond = cond
		self.true_block = true_block
		self.false_block = false_block
	def interp():
		if (self.cond.interp()):
			self.true_block.interp()
		else:
			self.false_block.interp()

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
			raise "Unknown operator {}".format(op)
		self.op = opToFn[op]
		self.lhs = lhs
		self.rhs = rhs
	def interp():
		return self.op(lhs.interp(), rhs.interp())

class Constant:
	def __init__(self, constant):
		self.constant = constant
	def interp():
		return self.constant
	
class Page:

