#!/usr/bin/env python
def main():
	arg = raw_input("Enter a word: ")

	ords = [ord(l) for l in arg]

	num = len(ords)
	for i in range(1, num):
		if ords[i - 1] == ords[i]:
			new = ords[i] - 5
			if new < 97:
				new += 26
			ords[i] = new
	print ''.join([chr(l) for l in ords])

if __name__ == '__main__':
	try:
		while True:
			main()
	except KeyboardInterrupt:
		print ''
