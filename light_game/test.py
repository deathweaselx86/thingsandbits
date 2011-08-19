#!/usr/bin/python
import frac
a = []
k = 3
n = pow(k,2)
b = 0
while b < k:
	m = 0
	a.append([])
	while m < 2:
		a[b].append([])
		m = m+1
	b = b+1
b = 0
while b < n:
	a[b/k][0].append(frac.Frac(1))
	b = b+1
b = 0
while b < k:
	a[b][1].append(frac.Frac(0))
	b = b+1
frac.printmat(a)
frac.rref(a)
frac.printmat(a)
print " ",a
if(a[2][0][1]== frac.Frac(0)):
	print "True"
else:
	print "False"
