#!/bin/python
# Get a matrix into row-reduced echelon form.

import string

def gcf(a, b):
	(a, b) = (abs(int(a)), abs(int(b)))
	if b > a: (a, b) = (b, a)
	while b > 0: (a, b) = (b, a%b)
	return a

class Frac:
	top = 0
	bottom = 1

	def __init__(self, top, bottom = 1):
		self.top = top
		self.bottom = bottom
		self.normalise()

	def __str__(self):
		if self.bottom == 1:
			return str(self.top)
		else:
			return str(self.top) + "/" + str(self.bottom)

	def normalise(self):
		if self.bottom < 0:
			self.top = -self.top
			self.bottom = -self.bottom
		f = gcf(self.top, self.bottom)
		self.top /= f
		self.bottom /= f

	def float(self):
		return (1.0 * self.top) / self.bottom

	def __mul__(self, b):
		return Frac(self.top * b.top, self.bottom * b.bottom)
	def __div__(self, b):
		return Frac(self.top * b.bottom, self.bottom * b.top)
	def __add__(self, b):
		bottom = self.bottom * b.bottom
		return Frac((self.top * b.bottom) + (b.top * self.bottom),
		            bottom)
	def __sub__(self, b):
		bottom = self.bottom * b.bottom
		return Frac((self.top * b.bottom) - (b.top * self.bottom),
		            bottom)
	def __neg__(self):
		return Frac(-self.top, self.bottom)

xtm = [[[Frac(2),Frac(3),Frac(-1)],[Frac(5)]],
       [[Frac(1),Frac(-2),Frac(4)],[Frac(2)]]]
ytm = [[[Frac(1),Frac(-2),Frac(1),Frac(1),Frac(-2)],[Frac(2)]],
      [[Frac(3),Frac(2),Frac(-2),Frac(2),Frac(-1)],[Frac(3)]],
      [[Frac(2),Frac(4),Frac(-3),Frac(1),Frac(1)],[Frac(1)]]]
lam = 1
tm = [[[Frac(1),Frac(-2),Frac(2)],[Frac(3)]],
      [[Frac(3),Frac(lam),Frac(-1)],[Frac(4)]],
      [[Frac(2),Frac(4),Frac(-3)],[Frac(2)]]]
test = [[[Frac(1),Frac(0),Frac(1),Frac(0)],[Frac(0)]],
	[[Frac(0),Frac(1),Frac(0),Frac(0)],[Frac(0)]],
	[[Frac(1),Frac(0),Frac(1),Frac(0)],[Frac(0)]],
	[[Frac(0),Frac(0),Frac(0),Frac(1)],[Frac(0)]]]
    
def mulrow(a, f): return [x * f for x in a]
def divrow(a, f): return [x / f for x in a]
def addrows(a, b): return [x + y for (x,y) in zip(a,b)]
def rowzero(l): return reduce(lambda x,y: x and y,[i.float() == 0 for i in l])

def explist(l): return string.join(map(lambda x: "%6s "%(str(x)), l))
def printmat(mat):
	for row in mat: print explist(row[0]), "|", explist(row[1])

def rref(mat):
	print "Before rref:" 
	printmat(mat)
	for i in range(len(mat)):
		m = mat[i]

		# Produce a leading one.
		f = m[0][i]
		if f.float() != 1 and f.float() != 0:
			print "Row", i, "divided by", f
			m[0] = divrow(m[0], f)
			m[1] = divrow(m[1], f)
			printmat(mat)

		# Go through the list making zeroes in the column.
		if rowzero(m[0]): continue
		for j in range(len(mat)):
			if j == i: continue
			mp = mat[j]
			f = -mp[0][i]
			if f.float() != 0:
				print "Row", i, "times", f, "added to row", j
				mp[0] = addrows(mp[0], mulrow(m[0], f))
				mp[1] = addrows(mp[1], mulrow(m[1], f))
				printmat(mat)

if __name__ == "__main__":
	print "Should be 18: ", gcf(54, 198)
	f = Frac(5,8) + Frac(3,8)
	print "Should be 1/1: ", f
	f += Frac(3,8)
	print "Should be 11/8: ", f
	rref(tm)
	rref(test)

