import math
class Point:
	def __init__(self,x,y):
		self.x = x
		self.y = y
	def __mul__(self,pt):
		return self.x*pt.x + self.y*pt.y
	def __add__(self,pt):
		return Point(self.x + pt.x, self.y + pt.y)
	def __sub__(self,pt):
		return Point(self.x - pt.x, self.y - pt.y)
	def __abs__(self):
		return math.sqrt(math.pow(self.x,2) + math.pow(self.y,2))
	def __neg__(self):
		return Point(-self.x,-self.y)
