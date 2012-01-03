
class Std:

	def __init__(self, out = '', err = '', code = 0):
		self.out = out
		self.err = err
		self.code = code

	
	def set(self, out, err, code = 0):
		self.out = out
		self.err = err
		self.code = code

	def __repr__(self):
		return "Stdout : %s\n\nStdErr : %s\n" % (self.out, self.err, self.code)

	def __str__(self):
		return self.__repr__()