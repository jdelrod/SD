# Exercise 4 Template
import os

# Do not modify the file name or function header

# Return the size of the file and words ending in 's'
def get_file_info(filename):
	# Your code here
	try:
		os.path.exists(filename)
	except OSError:
		raise

	if filename is None or type(filename) is not str:
		raise TypeError

	# Añadimos en size el tamaño en bytes del fichero filename
	size = os.path.getsize(filename)

	with open(filename, "r") as f:
		lista_ini = f.read().split()

	# Añadimos en wordlist aquellos valores cuyo contenido terminan con -s
	wordlist = []
	for value in lista_ini:
		if str(value).endswith("s"):
			wordlist.append(value)

	return size, wordlist
