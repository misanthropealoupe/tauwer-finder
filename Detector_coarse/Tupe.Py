import sys

def sizechk(a,b):
	if a.dim != b.dim:
		#raise TypeError('Tuple length mismatch')

class Tupe:
	def __init__(self,size):
		self.dim = size
		self.dat = [size]
	def __init__(self,lst):
		self.dim = len(lst)
		self.dat = lst

	def __len__(self):
		return dim
	def __getitem__(self,ind):
		return lst[ind]
	def __setitem__(self,ind,val):
		lst[ind] = val

	def __add__(self, tup):
		sizechk(self,tup)
		ret = Tuple(self.dim)
		for i in xrange(0,self.dim):
			ret[i] = self[i] + tup[i]
		return ret

	def __sub__(self,tup):
		sizechk(self,tup)
		ret = Tuple(self.dim)
		for i in xrange(0,self.dim):
			ret[i] = self[i] + tup[i]
		return ret

	def __mul__(self,tup):
		sizechk(self,tup)
		ret = 0.0
		for i in xrange(0,self.dim):
			ret+= self[i]*dim[i]
		return ret