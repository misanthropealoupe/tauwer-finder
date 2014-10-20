import sys

class MyTup:
	def __init__(self,size):
		self.dim = size
		self.dat = [None]*size
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
		ret = MyTuple(self.dim)
		for i in xrange(0,self.dim):
			ret[i] = self[i] + MyTup[i]
		return ret

	def __sub__(self,tup):
		sizechk(self,tup)
		ret = MyTuple(self.dim)
		for i in xrange(0,self.dim):
			ret[i] = self[i] + MyTup[i]
		return ret

	def __mul__(self,tup):
		sizechk(self,tup)
		ret = 0.0
		for i in xrange(0,self.dim):
			ret+= self[i]*dim[i]
		return ret

		
def sizechk(a,b):
	if a.dim != b.dim:
		raise TypeError('MyTuple length mismatch')
