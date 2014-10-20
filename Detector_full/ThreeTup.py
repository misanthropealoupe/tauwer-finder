import sys
import math

def sizechk(a,b):
	if a.dim != b.dim:
		raise TypeError('Tuple length mismatch')

class Tupe:
	def __init__(self,b):
		if isinstance(b,(list,tuple)):
			self.dim = len(b)
			self.dat = b
		else:
			self.dim = b
			self.dat = [None]*b	

	def __len__(self):
		return self.dim
	#def __getitem__(self,ind):
	#	return self.dat[ind]
	#def __setitem__(self,ind,val):
	#	self.dat[ind] = val

	#def __add__(self, tup):
	#	sizechk(self,tup)
	#	ret = Tupe(self.dim)
	#	for i in xrange(0,self.dim):
	#		ret[i] = self[i] + tup[i]
	#	return ret

	#def __sub__(self,tup):
	#	sizechk(self,tup)
	#	ret = Tupe(self.dim)
	#	for i in xrange(0,self.dim):
	#		ret[i] = self[i] - tup[i]
	#	return ret

	def __mul__(self,tup):
		if isinstance(tup,Tupe) and isinstance(self,Tupe):
			sizechk(self,tup)
			ret = self[0]*tup[0]
			for i in xrange(1,self.dim):
				ret+= self[i]*tup[i]
			return ret
		elif not isinstance(tup,Tupe):
			ret = Tupe(self.dim)
			ret[0] = self[0]*tup
			for i in xrange(1,self.dim):
				ret[i] = tup*self[i]
			return ret

class ThreeTup(Tupe):
	def __init__(self,lst=[None]*3):
		if len(lst) != 3:
			raise TypeError('Input list is not of length 3')
		#Tupe.__init__(self,lst)
		self.dat = lst
		self.dim = 3
	def __setitem__(self,ind,val):
		self.dat[ind] = val
	def __getitem__(self,ind):
		return self.dat[ind]
	def __add__(self,tup):
		if not isinstance(tup,ThreeTup):
			raise TypeError('Input argument is not a three-tuple')
		ret = ThreeTup([0,0,0])
		for i in xrange(0,3):
			ret[i] = self.__getitem__(i) + tup[i]
		return ret
	def __sub__(self,tup):
		if not isinstance(tup,ThreeTup):
			raise TypeError('Input argument is not a three-tuple')
		ret = ThreeTup([0,0,0])
		for i in xrange(0,3):
			ret[i] = self[i] - tup[i]
		return ret
	def __floordiv__(self,tup):
		if not isinstance(tup,ThreeTup):
			raise TypeError('Input argument is not a three-tuple')
		ret = ThreeTup()
		for i in xrange(0,3):
			ind = [(i+1)%3,(i+2)%3]
			ret[i] = self[ind[0]]*tup[ind[1]] - self[ind[1]]*tup[ind[0]]
		return ret
	def __abs__(self):
		norm = math.sqrt(self*self)
		if norm != 0.0:
			self = self*(1/norm)

	def __mul__(self,tup):
		if isinstance(tup,ThreeTup) and isinstance(self,ThreeTup):
			sizechk(self,tup)
			ret = self[0]*tup[0]
			for i in xrange(1,self.dim):
				ret+= self[i]*tup[i]
			return ret
		elif not isinstance(tup,ThreeTup):
			ret = ThreeTup()
			ret[0] = self[0]*tup
			for i in xrange(1,self.dim):
				ret[i] = tup*self[i]
			return ret

