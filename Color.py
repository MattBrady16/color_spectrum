import math

class Color:
	def __init__(self, r=0,g=0,b=0):
		rgb = [r, g, b]
		for element in rgb:
			if element > 255:
				element = 255
		self.r = int(r)
		self.g = int(g)
		self.b = int(b)

	# python denotes hexadecimal numbers as 0x ...
	# while tkinter denotes them as a string, # ...
	@classmethod
	def init_from_tkinter_hex(cls, args):
		int_color = int(args[1:], 16)
		r = math.floor(int_color/ (16 ** 4))
		g = math.floor((int_color % (16 ** 4))/ (16 ** 2))
		b = math.floor(int_color % (16 ** 2))
		color = cls(r,g,b)
		return color

	def to_hexa_int(self):
		return ((16 ** 4) * self.r) + ((16 ** 2) * self.g) + self.b;

	def to_hexa_str(self):
		return "{0:#0{1}x}".format(self.to_hexa_int(),8)[2:];

	def add_no_ceil(self, other):
		return Color(self.r+other.r, self.g+other.g, self.b+other.b)

	def __str__(self):
		return "#{0}".format(self.to_hexa_str())

	def __add__(self, other):
		rgbSelf = [self.r, self.g, self.b]
		rgbOther = [other.r, other.g, other.b]
		rgbOut = [0, 0, 0]
		for index in range(3):
			if rgbSelf[index] + rgbOther[index] > 255:
				rgbOut[index] = 255
			else:
				rgbOut[index] = rgbSelf[index] + rgbOther[index]
		return Color(rgbOut[0], rgbOut[1], rgbOut[2])

	def __sub__(self, other):
		rgbSelf = [self.r, self.g, self.b]
		rgbOther = [other.r, other.g, other.b]
		rgbOut = [0, 0, 0]
		for index in range(3):
			if rgbSelf[index] - rgbOther[index] < 0:
				rgbOut[index] = 0
			else:
				rgbOut[index] = rgbSelf[index] - rgbOther[index]
		return Color(rgbOut[0], rgbOut[1], rgbOut[2])

	def __mul__(self, other):
		rgbSelf = [self.r, self.g, self.b]
		rgbOut = [0, 0, 0]
		if isinstance(other, (int, float)):
			for index in range(3):
				if rgbSelf[index] * other > 255:
					rgbOut[index] = 255
				else:
					rgbOut[index] = rgbSelf[index] * other
			return Color(rgbOut[0], rgbOut[1], rgbOut[2])
		else:
			rgbOther = [other.r, other.g, other.b]
			for index in range(3):
				if rgbSelf[index] * rgbOther[index] > 255:
					rgbOut[index] = 255
				else:
					rgbOut[index] = rgbSelf[index] + rgbOther[index]
			return Color(rgbOut[0], rgbOut[1], rgbOut[2])

	def __truediv__(self, other):
		if isinstance(other, (int, float)):
			return Color(self.r/other, self.g/other, self.b/other)
		else:
			return Color(self.r/other.r, self.g/other.g, self.b/other.b)

	def __gt__(self, other):
		if isinstance(other, (int, float)):
			return Color(self.r/other, self.g/other, self.b/other)
		else:
			return Color(self.r/other.r, self.g/other.g, self.b/other.b)

	def sub_with_negative(self, other):
		return Color(self.r-other.r, self.g-other.g, self.b-other.b)

	# treat color like a vector
	def magnitude(self):
		return sqrt(self.r ** 2 + self.g ** 2 + self.b ** 2)

	# def pretty_print(self):
	# 	return "(r:{0},g:{1},b:{2})".format(self.r, self.g,self.b)
