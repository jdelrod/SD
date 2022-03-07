# Exercise 1 Template

# Do not modify the file name or function header

# Return the sum of those parameters that contain an even number
def accum(x, y, z):

	sum = 0
	if type(x) is not int or type(y) is not int or type(z) is not int:
		raise TypeError
	else:
		if x % 2 == 0:
			sum = sum+x
		if y % 2 == 0:
			sum = sum+y
		if z % 2 == 0:
			sum = sum+z

	return sum
